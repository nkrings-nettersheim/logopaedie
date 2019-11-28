import io
import logging
from datetime import datetime
from dateutil.parser import parse

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.views import generic
from reportlab.lib import colors
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph

from logopaedie.settings import BASE_DIR
from .forms import IndexForm, PatientForm, TherapyForm, ProcessReportForm, TherapyReportForm, DoctorForm
from .models import Patient, Therapy, Process_report, Therapy_report, Doctor

logger = logging.getLogger(__name__)

##########################################################################
# Area start and patient search
##########################################################################


def index(request):
    logger.info('Indexseite wurde geladen')
    form = IndexForm()
    return render(request, 'reports/index.html', {'form': form})


class PatientView(generic.ListView):
    model = Patient
    template_name = 'reports/patients.html'
    context_object_name = 'patients_list'
    logger.info('Patientenliste geladen')
    def get_queryset(self):
        return Patient.objects.all()


def search_patient(request):
    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            last_name = request.POST['last_name']
            date_of_birth = request.POST['date_of_birth']
            logger.info('search_patient: Suchkriterien: Nachname: ' + last_name + ' ; Geburtsdatum: ' + date_of_birth)
            if last_name != "":
                patients_list = Patient.objects.filter(pa_last_name__startswith=last_name)
                if len(patients_list) > 1:
                    logger.info("search_patient: Mehrere Patienten mit dem Nachnamen " + last_name + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.info("search_patient: Patient mit dem Suchbegriff: " + last_name + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.info("search_patient: Kein Patient mit dem Nachnamen: " + last_name + " gefunden")
                    return redirect('/reports/')
            elif date_of_birth != "":
                #datum = parse_date(date_of_birth)
                #assert False
                patients_list = Patient.objects.filter(pa_date_of_birth=parse(date_of_birth, dayfirst=True))
                if len(patients_list) > 1:
                    logger.info("search_patient: Mehrere Patienten mit dem Geburtsdatum " + date_of_birth + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.info("search_patient: Patient mit dem Geburtsdatum: " + date_of_birth + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.info("search_patient: Kein Patient mit dem Geburtsdatum: " + last_name + " gefunden")
                    return redirect('/reports/')

            else:
                logger.info("search_patient: Kein Suchkriterium eingegeben ")
                return redirect('/reports/')
    else:
        logger.info("search_patient: Kein POST Befehl erhalten")
        return redirect('/reports/')
    return render(request, 'reports/index.html', {'form': form})


##########################################################################
# Area Doctor create and change
##########################################################################


def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor_item = form.save(commit=False)
            doctor_item.save()
            logger.info("add_doctor: Arzt mit Namen: " + str(doctor_item.doctor_name1) + " angelegt")
            return redirect('/reports/doctor/' + str(doctor_item.id) + '/')
    else:
        logger.info('add_doctor: Formular zur Bearbeitung/Erfassung der Arztdaten')
        form = DoctorForm()
    return render(request, 'reports/doctor_form.html', {'form': form})


def search_doctor(request):
    if request.method == 'POST':
        name1 = request.POST['name1']
        if name1 != "":
            doctors_list = Doctor.objects.filter(doctor_name1__icontains=name1)
            if len(doctors_list) > 1:
                logger.info('search_doctor: mehr als einen Arzt gefunden mit dem Suchbegriff: ' + name1)
                return render(request, 'reports/doctors.html', {'doctors_list': doctors_list})
            elif len(doctors_list) == 1:
                logger.info('search_doctor: Arzt gefunden mit dem Suchbegriff: ' + name1)
                return redirect('/reports/doctor/' + str(doctors_list[0].id) + '/')
            else:
                logger.info('search_doctor: Keinen Arzt gefunden mit dem Suchbegriff: ' + name1)
                return render(request, 'reports/doctor_search.html')

        else:
            logger.info('search_doctor: Keinen Suchbegriff eingegeben:')
            return render(request, 'reports/doctor_search.html')
    else:
        logger.info('search_doctor: Keinen Suchbegriff eingegeben')
        return render(request, 'reports/doctor_search.html')


def edit_doctor(request, id=None):
    item = get_object_or_404(Doctor, id=id)
    form = DoctorForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('edit_doctor: Daten werden gespeichert')
        return redirect('/reports/doctor/' + str(item.id) + '/')
    logger.info('edit_doctor: Bearbeitungsformular aufgerufen ID: ' + id)
    return render(request, 'reports/doctor_form.html', {'form': form})


def doctor(request, id=id):
    try:
        doctor_result = Doctor.objects.get(id=id)
        logger.info('doctor: Arzt mit der ID: ' + id + ' aufgerufen')
        return render(request, 'reports/doctor.html', {'doctor': doctor_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')

##########################################################################
# Area Patient create and change
##########################################################################


def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_item = form.save(commit=False)
            patient_item.save()
            logger.info('add_patient: Patient mit der ID:' + str(patient_item.id) + ' gespeichert')
            return redirect('/reports/patient/' + str(patient_item.id) + '/')
    else:
        logger.info('add_patient: Formular aufgerufen')
        form = PatientForm()
    return render(request, 'reports/patient_form.html', {'form': form})


def edit_patient(request, id=None):
    item = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('edit_patient: Patient mit der ID:' + str(item.id) + ' geändert')
        return redirect('/reports/patient/' + str(item.id) + '/')
    logger.info('edit_patient: Patient mit der ID: ' + str(id) + ' zwecks Änderung aufgerufen')
    return render(request, 'reports/patient_form.html', {'form': form})


def patient(request, id=id):
    try:
        patient_result = Patient.objects.get(id=id)
        patient_helper = patient_result.id
        therapy_result = Therapy.objects.filter(patients_id=patient_helper).order_by('-recipe_date')
        therapy_result_count = therapy_result.count()
        process_result_count = 0
        for therapy_result_item in therapy_result:
            process_result_count = Process_report.objects.filter(therapy_id=therapy_result_item.id).count() + process_result_count
        logger.info('patient: Patient mit der ID: ' + str(id) + ' aufgerufen')
        return render(request, 'reports/patient.html', {'patient': patient_result,
                                                        'therapy': therapy_result,
                                                        'therapy_count': therapy_result_count,
                                                        'process_count': process_result_count})
    except ObjectDoesNotExist:
        logger.info('patient: Objekt existiert nicht')
        return redirect('/reports/')


##########################################################################
# Area Therapy create and change
##########################################################################


def add_therapy(request):
    if request.method == "POST":
        form = TherapyForm(request.POST)
        patient_result = Patient.objects.get(id=request.POST.get('patients'))
        if form.is_valid():
            therapy_item = form.save(commit=False)
            therapy_item.save()
            logger.info('add_therapy: Rezept für Patient mit ID: ' + str(patient_result.id) + ' angelegt')
            return redirect('/reports/patient/' + str(patient_result.id) + '/')
    else:
        logger.info('add_therapy: Formular aufgerufen um eine Rezept anzulegen')
        form = TherapyForm(initial={'patients': request.GET.get('id')})
        patient_result = Patient.objects.get(id=request.GET.get('id'))
    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': patient_result})


def edit_therapy(request, id=None):
    item = get_object_or_404(Therapy, id=id)
    form = TherapyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('edit_therapy: Rezept mit der ID:' + str(item.id) + ' geändert')
        return redirect('/reports/therapy/' + str(item.id) + '/')
    logger.info('edit_therapy: Rezeptformular des Patienten mit der ID: ' + str(item.id) + ' zwecks Änderung aufgerufen')
    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': item.patients})


def therapy(request, id=id):
    therapy_result = Therapy.objects.get(id=id)
    patient_value = Patient.objects.get(id=str((therapy_result.patients_id)))
    process_report_value = Process_report.objects.filter(therapy_id=id)
    if Therapy_report.objects.filter(therapy_id=id).exists():
        therapy_report_value = Therapy_report.objects.get(therapy_id=id)
    else:
        therapy_report_value = ''
    logger.info('therapy: Rezept mit der ID: ' + str(id) + ' aufgerufen')
    return render(request, 'reports/therapy.html', {'therapy': therapy_result,
                                                    'patient': patient_value,
                                                    'therapy_report': therapy_report_value,
                                                    'process_report': process_report_value})


##########################################################################
# Area Process Report (in German: Verlaufsprotokol)
##########################################################################


def add_process_report(request):
    if request.method == "POST":
        form = ProcessReportForm(request.POST)
        if form.is_valid():
            therapy_report_item = form.save(commit=False)
            therapy_report_item.save()
            logger.info('add_process_report: Verlaufsprotokoll gespeichert mit ID: ' + str(request.POST.get('therapy')))
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/')
    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = ProcessReportForm(
            initial={'process_treatment': Process_report.objects.filter(therapy_id=request.GET.get('id')).count() + 1,
                     'therapy': therapy_result})
        logger.info('add_process_report: Verlaufsprotokoll anlegen mit ID: ' + request.GET.get('id'))
        return render(request, 'reports/process_report_form.html', {'form': form})


def edit_process_report(request, id=None):
    item = get_object_or_404(Process_report, id=id)
    form = ProcessReportForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('edit_process_report: Verlaufsprotokoll ändern mit ID: ' + str(item.id))
        return redirect('/reports/process_report/' + str(item.id) + '/')
    logger.info('edit_process_report: Verlaufsprotokoll anlegen mit ID: ' + id)
    return render(request, 'reports/process_report_form.html', {'form': form})


def process_report(request, id=id):
    process_report = Process_report.objects.get(id=id)
    logger.info('process_report: Verlaufsprotokoll mit ID: ' + id + ' anzeigen')
    return render(request, 'reports/process_report.html', {'process_report': process_report})


def show_process_report(request):
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleNC = styles['Normal']
    styleNC.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    def coord(x, y, height,  unit=1):
        x, y = x * unit, height - y * unit
        return x, y

    id = request.GET.get('id')
    logger.info('show_process_report: Verlaufsprotokoll mit ID: ' + id + ' gedruckt')
    therapy_value = Therapy.objects.get(id=id)
    pa_first_name = Therapy.objects.get(id=id).patients.pa_first_name
    pa_last_name = Therapy.objects.get(id=id).patients.pa_last_name
    process_report_value = Process_report.objects.values_list('process_treatment',
                                                             'process_content',
                                                             'process_exercises',
                                                             'process_results'
                                                              ).filter(therapy=id)
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont('Helvetica', 18)
    p.drawString(6 * cm, 28 * cm, "Therapieverlaufdokumentation")
    p.setFont('Helvetica', 14)
    p.drawString(1.5 * cm, 27 * cm, "Rezept - Datum: " + str(therapy_value.recipe_date.strftime("%d.%m.%Y")))
    p.drawString(14 * cm, 27 * cm, "Patient: " + pa_last_name + ", " + pa_first_name)
    p.setFont('Helvetica', 10)
    p.drawString(1.5 * cm, 1 * cm, "Bericht: ")
    p.drawString(11 * cm, 1 * cm, "Behandlung von: " +
                 str(therapy_value.therapy_start.strftime("%d.%m.%Y")) +
                 " bis: " +
                 str(therapy_value.therapy_end.strftime("%d.%m.%Y")))
    p.drawString(1.5 * cm, 0.5 * cm, "Druckdatum: " + str(datetime.now().strftime("%d.%m.%Y %H:%M")))


    # initiate data list
    data = []

    # create Headers
    htreatment = Paragraph('''Behand- lung''', styleBH)
    hcontent = Paragraph('''Therapieinhalt''', styleBH)
    hexercises = Paragraph('''Übungen''', styleBH)
    hresult = Paragraph('''Ergebnis  + ; - ; 0''', styleBH)

    # write header to data
    data.append([htreatment, hcontent, hexercises, hresult])

    # write contentelements to data
    for item in list(process_report_value):
        ctreatment = Paragraph((str(item[0])), styleNC)
        ccontent = Paragraph((str(item[1])), styleN)
        cexercises = Paragraph((str(item[2])), styleNC)
        cresult = Paragraph((str(item[3])), styleNC)
        data.append([ctreatment, ccontent, cexercises, cresult])

    #create table
    table = Table(data, colWidths=[2 * cm, 12.5 * cm, 2 * cm,
                                   2 * cm])

    table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ]))
    w, h = table.wrap(width, height)
    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(1.5, 3, height - h, cm))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    file_name = pa_last_name + "_" + pa_first_name + "_" + str(therapy_value.recipe_date) + ".pdf"
    return FileResponse(buffer, as_attachment=True, filename=file_name)


##########################################################################
# Area Therapyreport (in German: Therapiebericht)
##########################################################################


def add_therapy_report(request):
    if request.method == "POST":
        form = TherapyReportForm(request.POST)
        if form.is_valid():
            therapy_report_item = form.save(commit=False)
            therapy_report_item.save()
            logger.info('add_therapy_report: Therapiebericht gespeichert mit ID: ' + str(request.POST.get('therapy')))
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/')
        else:
            print('not valid')
            return render(request, 'reports/therapy_report_form.html', {'form': form})

    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = TherapyReportForm(
            initial={'therapy': therapy_result})
        logger.info('add_therapy_report: Therapiebericht gespeichert mit ID: ' + str(request.POST.get('therapy')))
        return render(request, 'reports/therapy_report_form.html', {'form': form})


def edit_therapy_report(request, id=None):
    item = get_object_or_404(Therapy_report, id=id)
    form = TherapyReportForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('edit_therapy_report: Therapiebericht ändern mit ID: ' + str(id))
        return redirect('/reports/therapy/' + str(item.therapy_id) + '/')
    logger.info('edit_therapy_report: Therapybericht anlegen mit ID: ' + id)
    return render(request, 'reports/therapy_report_form.html', {'form': form})


def therapy_report(request, id=id):
    therapy_report = Therapy_report.objects.get(id=id)
    logger.info('therapy_report: Therapiebericht mit ID: ' + id + ' anzeigen')
    return render(request, 'reports/therapy_report.html', {'therapy_report': therapy_report})


def show_therapy_report(request):
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleNC = styles['Normal']
    styleNC.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    def coord(x, y, height,  unit=1):
        x, y = x * unit, height - y * unit
        return x, y

    pdfmetrics.registerFont(TTFont('TNRB', 'Times New Roman Bold.ttf'))

    id = request.GET.get('id')
    logger.info('show_therapy_report: Therapiebericht mit ID: ' + id + ' gedruckt')
    therapy_result = Therapy.objects.get(id=id)
    pa_first_name = Therapy.objects.get(id=id).patients.pa_first_name
    pa_last_name = Therapy.objects.get(id=id).patients.pa_last_name
    pa_date_of_birth = Therapy.objects.get(id=id).patients.pa_date_of_birth
    recipe_date = Therapy.objects.get(id=id).recipe_date
    therapy_start = Therapy.objects.get(id=id).therapy_start
    therapy_end = Therapy.objects.get(id=id).therapy_end

    process_count = Process_report.objects.filter(therapy=id).count()

    result = Therapy_report.objects.get(therapy=id)

    doctor_result = Doctor.objects.get(id=therapy_result.therapy_doctor_id)

    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    p.setFillColorRGB(0.66, 0.50, 0.82)
    p.rect(0, 0, 20, 850, fill=True, stroke=False)
    p.rect(200, 822, 400, 20, fill=True, stroke=False)

    p.setFillColor(black)
    p.setFont('Helvetica', 12)
    p.drawString(2.2 * cm, 3.3 * cm, "Mit freundlichen Grüßen")
    p.setFont('Helvetica-Bold', 12)
    p.drawString(2.2 * cm, 19.7 * cm, "Mitteilung des Therapeuten an den verordnenden Arzt:")
    p.drawString(2.2 * cm, 16.7 * cm, "Aktueller Stand der Therapie:")
    p.drawString(2.2 * cm, 23.5 * cm, str(doctor_result.doctor_name1))
    p.drawString(2.2 * cm, 23.0 * cm, str(doctor_result.doctor_name2))
    p.drawString(2.2 * cm, 22.0 * cm, str(doctor_result.doctor_street))
    p.drawString(2.2 * cm, 21.5 * cm, str(doctor_result.doctor_zip_code) + " " + str(doctor_result.doctor_city))


    p.line(2.2 * cm, 16.6 * cm, 8.15 * cm, 16.6 * cm)
    p.drawString(2.2 * cm, 13.7 * cm, "Therapieschwerpunkte:")
    p.line(2.2 * cm, 13.6 * cm, 7.0 * cm, 13.6 * cm)
    p.drawString(2.2 * cm, 11.1 * cm, "Prognostische Einschätzung mit Angabe der Restsymptomatik:")
    p.line(2.2 * cm, 11.0 * cm, 15.0 * cm, 11.0 * cm)
    p.drawString(2.2 * cm, 4.0 * cm, "Bei Fragen stehe ich Ihnen jeder Zeit zur Verfügung!")
    p.drawString(11 * cm, 2.3 * cm, "Vielen Dank für die Kooperation")

    p.setFont('Helvetica-Bold', 10)
    p.drawString(12.8 * cm, 22.3 * cm, "Euskirchen den: " + str(datetime.now().strftime("%d.%m.%Y")))
    p.drawString(2.2 * cm, 18.9 * cm, "Name des Patienten:")
    p.drawString(11.2 * cm, 18.9 * cm, "geb. am:")
    p.drawString(2.2 * cm, 18.4 * cm, "Rezeptdatum:")
    p.drawString(2.5 * cm, 17.9 * cm, "Behandlungen vom:")
    p.drawString(12.0 * cm, 17.9 * cm, "bis:")
    p.drawString(2.2 * cm, 17.4 * cm, "Indikationsschlüssel:")
    p.drawString(11.1 * cm, 17.4 * cm, "ICD-Cod:")
    p.drawString(2.2 * cm, 6.6 * cm, "Behandlung weiter indiziert:")
    p.drawString(2.2 * cm, 5.8 * cm, "Pause:")
    p.drawString(10.2 * cm, 5.8 * cm, "Fortsetzung ab:")
    p.drawString(2.2 * cm, 5.0 * cm, "Bemerkung:")

    p.setFont('Helvetica', 10)
    p.drawString(6.2 * cm, 18.9 * cm, pa_last_name + ", " + pa_first_name)
    p.drawString(13.2 * cm, 18.9 * cm, str(pa_date_of_birth.strftime("%d.%m.%Y")))
    p.drawString(6.2 * cm, 18.4 * cm, str(recipe_date.strftime("%d.%m.%Y")))
    p.drawString(6.2 * cm, 17.9 * cm, str(therapy_start.strftime("%d.%m.%Y")))
    p.drawString(13.2 * cm, 17.9 * cm, str(therapy_end.strftime("%d.%m.%Y")))
    p.drawString(2.2 * cm, 17.9 * cm, str(process_count))
    p.drawString(6.2 * cm, 17.4 * cm, str(therapy_result.therapy_indication_key))
    p.drawString(13.2 * cm, 17.4 * cm, str(therapy_result.therapy_icd_cod))
    p.drawString(6.2 * cm, 5.0 * cm, str(result.therapy_comment))

    if result.therapy_break_date:
        p.drawString(14.0 * cm, 5.8 * cm, str(result.therapy_break_date.strftime("%d.%m.%Y")))

    if result.therapy_indicated:
        p.drawString(8.12 * cm, 6.6 * cm, "X")

    if result.therapy_break:
        p.drawString(8.12 * cm, 5.8 * cm, "X")

    p.setFont('Helvetica', 8)
    p.drawString(2.8 * cm, 24.7 * cm, "Logopädie Praxis Petra Klein - Rathausstrasse 8 - 53879 Euskirchen")

    p.setFillColorRGB(0.66, 0.5, 0.82)
    p.setFont('Helvetica', 10)
    p.drawString(4.0 * cm, 26.4 * cm, "Behandlungen von Sprach-, Stimm-, Sprech- und Schluckstörungen")
    p.drawString(4.0 * cm, 25.9 * cm, "sowie Mutismus")

    #RGB Wert wird errechnet aus RGB Wert / 256
    p.setFillColorRGB(0.66, 0.66, 0.66)
    p.setFont('TNRB', 22)
    p.drawString(4.0 * cm, 27.8 * cm, "Petra Klein")
    p.drawString(4.0 * cm, 27.1 * cm, "Staatlich geprüfte Logopädin")
    p.setFont('TNRB', 18)
    p.drawString(13.2 * cm, 29.15 * cm, "seit 1987")

    p.setFont('Helvetica', 10)
    p.drawString(15.3 * cm, 28.0 * cm, "Rathausstrasse 8")
    p.drawString(15.3 * cm, 27.6 * cm, "53879 Euskirchen")
    p.drawString(15.3 * cm, 27.0 * cm, "Tel.")
    p.drawString(16.6 * cm, 27.0 * cm, "02251 / 5 97 62")
    p.drawString(15.3 * cm, 26.5 * cm, "Fax.")
    p.drawString(16.6 * cm, 26.5 * cm, "02251 / 7 15 11")
    p.drawString(15.3 * cm, 25.5 * cm, "Bahnhofstrasse 26")
    p.drawString(15.3 * cm, 25.1 * cm, "53947 Nettersheim")
    p.drawString(15.3 * cm, 24.4 * cm, "Tel.")
    p.drawString(16.6 * cm, 24.4 * cm, "02486 / 80 29 50")
    p.drawString(15.3 * cm, 23.8 * cm, "Fax.")
    p.drawString(16.6 * cm, 23.8 * cm, "02486 / 80 29 60")

    p.drawInlineImage(BASE_DIR + '/reports/static/reports/images/logopaedie.jpeg', 1.3 * cm, 25.6 * cm, width=2.12 * cm, height=3.72 * cm)
    p.drawInlineImage(BASE_DIR + '/reports/static/reports/images/unterschrift.jpeg', 3.0 * cm, 1.5 * cm, width=4.0 * cm, height=1.74 * cm)
    p.setStrokeColor(black)
    p.grid([8.0*cm, 8.5*cm], [6.5*cm, 7.0*cm])
    p.grid([8.0*cm, 8.5*cm], [5.7*cm, 6.2*cm])

    data = []
    content = str(str(result.therapy_current_result)).replace('\n', '<br />\n')
    ccontent = Paragraph(content, styleN)
    data.append([ccontent])

    table = Table(data, colWidths=[18 * cm])

    w, h = table.wrap(width, height)
    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(2.0, 13.0, height - h, cm))

    data = []
    content = str(str(result.therapy_emphases)).replace('\n', '<br />\n')
    ccontent = Paragraph((content), styleN)
    data.append([ccontent])


    table = Table(data, colWidths=[18 * cm])

    w, h = table.wrap(width, height)
    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(2.0, 16.0, height - h, cm))

    data = []
    content = str(str(result.therapy_forecast)).replace('\n', '<br />\n')
    ccontent = Paragraph(content, styleN)
    #ccontent = str(ccontent).replace('\n', '<br />\n')
    data.append([ccontent])

    table = Table(data, colWidths=[18 * cm])

    w, h = table.wrap(width, height)
    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(2.0, 18.6, height - h, cm))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    file_name = pa_last_name + "_" + pa_first_name + "_" + str(recipe_date) + ".pdf"
    return FileResponse(buffer, as_attachment=True, filename=file_name)



# **************************************************************************************************

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-23s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': BASE_DIR + '/logopaedie.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'django.security.*': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
})
