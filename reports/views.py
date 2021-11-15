import io
import os
import logging
import datetime
import locale

from html import escape
from dateutil.parser import parse
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.conf import settings
from django.views import generic
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.core.mail import send_mail

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph

from weasyprint import HTML, CSS

from logopaedie.settings import BASE_DIR, X_FORWARD

from .forms import IndexForm, PatientForm, TherapyForm, ProcessReportForm, TherapyReportForm, DoctorForm, \
    TherapistForm, SearchDoctorForm, SearchTherapistForm, InitialAssessmentForm, DocumentForm, TherapySomethingForm, \
    DocumentTherapyForm, PatientSomethingForm, Diagnostic_groupForm, SearchDiagnostic_groupForm, \
    WaitlistForm

from .models import Patient, Therapy, Process_report, Therapy_report, Doctor, Therapist, InitialAssessment, Document, \
    Therapy_Something, Document_therapy, Patient_Something, Login_Failed, Diagnostic_group, Wait_list

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, "de_DE")

##########################################################################
# Area start and patient search
##########################################################################

@login_required
def index(request):
    logger.debug('Indexseite wurde geladen')
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    form = IndexForm()
    return render(request, 'reports/index.html', {'form': form})


def impressum(request):
    logger.debug('Impressumseite aufgerufen')
    return render(request, 'reports/impressum.html')


class PatientView(generic.ListView):
    model = Patient
    template_name = 'reports/patients.html'
    context_object_name = 'patients_list'
    logger.debug('Patientenliste geladen')

    def get_queryset(self):
        return Patient.objects.all()


##########################################################################
# open Reports
##########################################################################
@login_required
def open_reports(request):
    therapist_value = Therapist.objects.filter(tp_user_logopakt=str(request.user))
    if therapist_value:
        therapy_list = Therapy.objects.filter(therapists=therapist_value[0].id,
                                              therapy_report_no_yes=True).order_by('recipe_date')
    else:
        therapy_list = Therapy.objects.filter(therapy_report_no_yes=True).order_by('recipe_date')
    reports_list = []
    for tp_item in therapy_list:
        report_date_value = ''
        process_report_value = Process_report.objects.filter(therapy=tp_item.id)
        process_report_value_count = process_report_value.count()
        tp_item.prvc = process_report_value_count
        quotient = process_report_value_count / int(tp_item.therapy_regulation_amount)
        if quotient > 0.6:
            therapy_report_result = Therapy_report.objects.filter(therapy_id=tp_item.id)
            try:
                report_date_value = therapy_report_result[0].report_date
            except:
                logger.debug("Try Exception")

            if not report_date_value:
                patient_value = Patient.objects.filter(id=tp_item.patients.id)
                tp_item.pa_last_name = patient_value[0].pa_last_name
                tp_item.pa_first_name = patient_value[0].pa_first_name
                reports_list.append(tp_item)
        logger.debug('verordnet: ' + str(tp_item.therapy_regulation_amount) +
                    ' ;Therapien: ' + str(process_report_value_count) +
                    ' Quotient: ' + str(quotient) +
                    ' report_date_value: ' + str(report_date_value))

    logger.debug('Open_Reports wurde geladen')
    return render(request, 'reports/open_reports.html', {'reports': reports_list})


##########################################################################
# therapy_breaks_internal
##########################################################################
@login_required
def therapy_breaks(request):
    if request.user.groups.filter(name='Leitung').exists():
        therapy_reports = Therapy_report.objects. \
            select_related('therapy__patients'). \
            select_related('therapy__therapists'). \
            filter(therapy_break_internal=True,
                   therapy_end__lte=datetime.date.today() + datetime.timedelta(days=-22),
                   therapy__patients__pa_active_no_yes=True).order_by('therapy_end')
    else:
        therapy_reports = Therapy_report.objects. \
            select_related('therapy__patients'). \
            select_related('therapy__therapists'). \
            filter(therapy_break_internal=True,
                   therapy_end__lte=datetime.date.today() + datetime.timedelta(days=-22),
                   therapy__therapists__tp_user_logopakt=str(request.user),
                   therapy__patients__pa_active_no_yes=True).order_by('therapy_end')

    time_green = datetime.datetime.now() + datetime.timedelta(days=-22)
    time_orange = datetime.datetime.now() + datetime.timedelta(days=-52)
    time_red = datetime.datetime.now() + datetime.timedelta(days=-92)
    print(f"grün: {time_green}; orange: {time_orange}; red: {time_red}")
    logger.debug('Open_Reports wurde geladen')
    return render(request, 'reports/therapy_breaks.html', {'breaks': therapy_reports,
                                                           'time_green': time_green,
                                                           'time_orange': time_orange,
                                                           'time_red': time_red
                                                           })

def update_report(request, id=None):
    report = get_object_or_404(Therapy_report, id=id)
    if report:
        report.therapy_break_internal = False
        report.save(update_fields=['therapy_break_internal'])
        return redirect('/reports/therapy_breaks/')
    return redirect('/reports/therapy_breaks/')


##########################################################################
# Area Doctor create and change
##########################################################################

@login_required
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor_item = form.save(commit=False)
            doctor_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_doctor: Arzt mit Namen: ' + str(
                doctor_item.doctor_name1) + ' angelegt')
            return redirect('/reports/doctor/' + str(doctor_item.id) + '/')
    else:
        logger.debug('add_doctor: Formular zur Bearbeitung/Erfassung der Arztdaten')
        form = DoctorForm()
    return render(request, 'reports/doctor_form.html', {'form': form})

@login_required
def search_doctor_start(request):
    logger.debug('Suchmaske Arzt geladen')
    form = SearchDoctorForm()
    return render(request, 'reports/doctor_search.html', {'form': form})

@login_required
def search_doctor(request):
    form = SearchDoctorForm()
    if request.method == 'POST':
        name1 = request.POST['name1']
        lanr = request.POST['lanr']
        if name1 != "":
            doctors_list = Doctor.objects.filter(Q(doctor_name1__icontains=name1) |
                                                 Q(doctor_name2__icontains=name1) |
                                                 Q(doctor_name3__icontains=name1))
            if len(doctors_list) > 1:
                logger.debug('search_doctor: mehr als einen Arzt gefunden mit dem Suchbegriff: ' + name1)
                return render(request, 'reports/doctors.html', {'doctors_list': doctors_list})
            elif len(doctors_list) == 1:
                logger.debug('search_doctor: Arzt gefunden mit dem Suchbegriff: ' + name1)
                return redirect('/reports/doctor/' + str(doctors_list[0].id) + '/')
            else:
                logger.debug('search_doctor: Keinen Arzt gefunden mit dem Suchbegriff: ' + name1)
                return render(request, 'reports/doctor_search.html', {'form': form})
        elif lanr != "":
            doctors_list = Doctor.objects.filter(doctor_lanr=lanr)
            if len(doctors_list) == 1:
                logger.debug('search_doctor: Arzt gefunden mit dem Suchbegriff: ' + lanr)
                return redirect('/reports/doctor/' + str(doctors_list[0].id) + '/')
            else:
                logger.debug('search_doctor: Keinen Arzt gefunden mit dem Suchbegriff: ' + lanr)
                return render(request, 'reports/doctor_search.html', {'form': form})
        else:
            logger.debug('search_doctor: Keinen Suchbegriff eingegeben:')
            return render(request, 'reports/doctor_search.html', {'form': form})
    else:
        logger.debug('search_doctor: Keinen Suchbegriff eingegeben')
        return render(request, 'reports/doctor_search.html')

@login_required
def edit_doctor(request, id=None):
    item = get_object_or_404(Doctor, id=id)
    form = DoctorForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_doctor: ' + str(item.id) + ' Daten werden gespeichert')
        return redirect('/reports/doctor/' + str(item.id) + '/')
    logger.debug('edit_doctor: Bearbeitungsformular aufgerufen ID: ' + id)
    form.id = item.id
    return render(request, 'reports/doctor_form.html', {'form': form})

@login_required
def doctor(request, id=id):
    try:
        doctor_result = Doctor.objects.get(id=id)
        logger.debug('doctor: Arzt mit der ID: ' + id + ' aufgerufen')
        return render(request, 'reports/doctor.html', {'doctor': doctor_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')


##########################################################################
# Area Therapist create and change
##########################################################################

@login_required
def add_therapist(request):
    if request.method == "POST":
        form = TherapistForm(request.POST)
        if form.is_valid():
            therapist_item = form.save(commit=False)
            therapist_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_therapist: Therapist mit Namen: ' + str(
                therapist_item.tp_last_name) + ' angelegt')
            return redirect('/reports/therapist/' + str(therapist_item.id) + '/')
    else:
        logger.debug('add_therapist: Formular zur Bearbeitung/Erfassung der Therapistdaten')
        form = TherapistForm()
    return render(request, 'reports/therapist_form.html', {'form': form})

@login_required
def search_therapist_start(request):
    logger.debug('Suchmaske Therapeut geladen')
    form = SearchTherapistForm()
    return render(request, 'reports/therapist_search.html', {'form': form})

@login_required
def search_therapist(request):
    form = SearchTherapistForm()
    if request.method == 'POST':
        kuerzel = request.POST['tp_initial']
        if kuerzel != "":
            therapists_list = Therapist.objects.filter(tp_initial__icontains=kuerzel)
            if len(therapists_list) > 1:
                logger.debug('search_therapist: mehr als einen Therapeut gefunden mit dem Suchbegriff: ' + kuerzel)
                return render(request, 'reports/therapists.html', {'therapists_list': therapists_list})
            elif len(therapists_list) == 1:
                logger.debug('search_therapist: Therpeut gefunden mit dem Suchbegriff: ' + kuerzel)
                return redirect('/reports/therapist/' + str(therapists_list[0].id) + '/')
            else:
                logger.debug('search_therapist: Keinen Therapeut gefunden mit dem Suchbegriff: ' + kuerzel)
                return render(request, 'reports/therapist_search.html', {'form': form})

        else:
            logger.debug('search_therapist: Keinen Suchbegriff eingegeben:')
            return render(request, 'reports/therapist_search.html', {'form': form})
    else:
        logger.debug('search_therapist: Keinen Suchbegriff eingegeben')
        return render(request, 'reports/therapist_search.html', {'form': form})

@login_required
def edit_therapist(request, id=None):
    item = get_object_or_404(Therapist, id=id)
    form = TherapistForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_therapist: ' + str(item.id) + ' Daten werden gespeichert')
        return redirect('/reports/therapist/' + str(item.id) + '/')
    logger.debug('edit_therapist: Bearbeitungsformular aufgerufen ID: ' + id)
    form.id = item.id
    return render(request, 'reports/therapist_form.html', {'form': form})

@login_required
def therapist(request, id=id):
    try:
        therapist_result = Therapist.objects.get(id=id)
        logger.debug('therapist: Therapeut mit der ID: ' + id + ' aufgerufen')
        return render(request, 'reports/therapist.html', {'therapist': therapist_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')

##########################################################################
# Area Diagnostic_group create and change
##########################################################################

@login_required
def add_diagnostic_group(request):
    if request.method == "POST":
        form = Diagnostic_groupForm(request.POST)
        if form.is_valid():
            diagnostic_group_item = form.save(commit=False)
            diagnostic_group_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_diagnostic_group: Diagnosticgruppe mit Namen: ' + str(
                diagnostic_group_item.diagnostic_key) + ' angelegt')
            return redirect('/reports/diagnostic_group/' + str(diagnostic_group_item.id) + '/')
    else:
        logger.debug('add_diagnostic_group: Formular zur Bearbeitung/Erfassung der Diagnosedaten')
        form = Diagnostic_groupForm()
    return render(request, 'reports/diagnostic_group_form.html', {'form': form})

@login_required
def search_diagnostic_group_start(request):
    logger.debug('Suchmaske Diagnosegruppe geladen')
    form = SearchDiagnostic_groupForm()
    return render(request, 'reports/diagnostic_group_search.html', {'form': form})

@login_required
def search_diagnostic_group(request):
    form = SearchDiagnostic_groupForm()
    if request.method == 'POST':
        diagnostic_key = request.POST['diagnostic_key']
        if diagnostic_key != "":
            diagnostic_group_list = Diagnostic_group.objects.filter(diagnostic_key__istartswith=diagnostic_key)

            if len(diagnostic_group_list) > 1:
                logger.debug('search_diagnostic_group: mehr als eine Diagnostic gefunden mit dem Suchbegriff: ' + diagnostic_key)
                return render(request, 'reports/diagnostic_groups.html', {'diagnostic_group_list': diagnostic_group_list})
            elif len(diagnostic_group_list) == 1:
                logger.debug('search_diagnostic_group: Diagnosticgruppe gefunden mit dem Suchbegriff: ' + diagnostic_key)
                return redirect('/reports/diagnostic_group/' + str(diagnostic_group_list[0].id) + '/')
            else:
                logger.debug('search_diagnostic_group: Keine Diagnosticgruppe gefunden mit dem Suchbegriff: ' + diagnostic_key)
                return render(request, 'reports/diagnostic_group_search.html', {'form': form})
        else:
            logger.debug('search_diagnostic_group: Keinen Suchbegriff eingegeben:')
            return render(request, 'reports/diagnostic_group_search.html', {'form': form})
    else:
        logger.debug('search_diagnostic_group: Keinen Suchbegriff eingegeben')
        return render(request, 'reports/diagnostic_group_search.html')

@login_required
def edit_diagnostic_group(request, id=None):
    item = get_object_or_404(Diagnostic_group, id=id)
    form = Diagnostic_groupForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_diagnostic_group: ' + str(item.id) + ' Daten werden gespeichert')
        return redirect('/reports/diagnostic_group/' + str(item.id) + '/')
    logger.debug('edit_diagnostic_group: Bearbeitungsformular aufgerufen ID: ' + id)
    form.id = item.id
    return render(request, 'reports/diagnostic_group_form.html', {'form': form})

@login_required
def diagnostic_group(request, id=id):
    try:
        diagnostic_group_result = Diagnostic_group.objects.get(id=id)
        logger.debug('diagnostic_group: Diagnosegruppe mit der ID: ' + id + ' aufgerufen')
        return render(request, 'reports/diagnostic_group.html', {'diagnostic_group': diagnostic_group_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')



##########################################################################
# Area Patient search, create and change
##########################################################################

@login_required
def search_patient(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")

    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            date_of_birth = request.POST['date_of_birth']
            phone = request.POST['phone']
            cell_phone = request.POST['cell_phone']
            try:
                if request.POST['active']:
                    active = True
            except:
                inactive = ''
            try:
                if request.POST['inactive']:
                    active = False
            except:
                inactive = ''
            try:
                if request.POST['active'] and request.POST['inactive']:
                    active = ''
            except:
                inactive = ''
            logger.debug('active: ' + str(active))
            data = request.POST['phone']
            if data:
                phone = data.replace(' ', '')

            data = request.POST['cell_phone']
            if data:
                cell_phone = data.replace(' ', '')

            if last_name != "":
                if active == True or active == False:
                    patients_list = Patient.objects.filter(pa_last_name__istartswith=last_name,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_last_name__istartswith=last_name).order_by('pa_last_name',
                                                                                                         'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug("search_patient: Mehrere Patienten mit dem Namen: " + last_name + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug("search_patient: Patient mit dem Suchbegriff: " + last_name + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug("search_patient: Kein Patient mit dem Nachnamen: " + last_name + " gefunden")
                    return redirect('/reports/')

            elif first_name != "":
                if active == True or active == False:
                    patients_list = Patient.objects.filter(pa_first_name__istartswith=first_name,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_first_name__istartswith=first_name).order_by(
                        'pa_last_name', 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug("search_patient: Mehrere Patienten mit dem Vornamen: " + first_name + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug(
                        "search_patient: Patient mit dem Suchbegriff: " + last_name + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug(
                        "search_patient: Kein Patient mit dem Nachnamen: " + last_name + " gefunden")
                    return redirect('/reports/')

            elif date_of_birth != "":
                if active == True or active == False:
                    patients_list = Patient.objects.filter(pa_date_of_birth=parse(date_of_birth, dayfirst=True),
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(
                        pa_date_of_birth=parse(date_of_birth, dayfirst=True)).order_by('pa_last_name', 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(
                        "search_patient: Mehrere Patienten mit dem Geburtsdatum " + date_of_birth + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug("search_patient: Patient mit dem Geburtsdatum: " + date_of_birth + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug("search_patient: Kein Patient mit dem Geburtsdatum: " + last_name + " gefunden")
                    return redirect('/reports/')

            elif phone != "":
                if active == True or active == False:
                    patients_list = Patient.objects.filter(pa_phone__istartswith=phone,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_phone__istartswith=phone).order_by('pa_last_name',
                                                                                                 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug("search_patient: Mehrere Patienten mit der Telefonnummer " + phone + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug("search_patient: Patient mit der Telefonnummer: " + phone + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug("search_patient: Kein Patient mit der Telefonnummer: " + phone + " gefunden")
                    return redirect('/reports/')

            elif cell_phone != "":
                if active == True or active == False:
                    patients_list = Patient.objects.filter(pa_cell_phone__istartswith=cell_phone,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_cell_phone__istartswith=cell_phone).order_by(
                        'pa_last_name', 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(
                        "search_patient: Mehrere Patienten mit der Mobilfunknummer " + cell_phone + " gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug("search_patient: Patient mit der Mobilfunknummer: " + cell_phone + " gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug("search_patient: Kein Patient mit der Mobilfunknummer: " + cell_phone + " gefunden")
                    return redirect('/reports/')

            else:
                logger.debug("search_patient: Kein Suchkriterium eingegeben ")
                return redirect('/reports/')
    else:
        logger.debug("search_patient: Kein POST Befehl erhalten")
        return redirect('/reports/')
    return render(request, 'reports/index_parents.html', {'form': form})


@login_required
def add_patient(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_item = form.save(commit=False)
            patient_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_patient: Patient mit der ID:' + str(
                patient_item.id) + ' gespeichert')
            return redirect('/reports/patient/' + str(patient_item.id) + '/')
    else:
        logger.debug('add_patient: Formular aufgerufen')
        form = PatientForm()
    return render(request, 'reports/patient_form.html', {'form': form})


@login_required
def edit_patient(request, id=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    item = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_patient: Patient mit der ID:' + str(item.id) + ' geändert')
        return redirect('/reports/patient/' + str(item.id) + '/')
    logger.debug('edit_patient: Patient mit der ID: ' + str(id) + ' zwecks Änderung aufgerufen')
    form.id = item.id
    return render(request, 'reports/patient_form.html', {'form': form})


@login_required
def patient(request, id=id):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    try:
        patient_result = Patient.objects.get(id=id)
        patient_helper = patient_result.id

        patient_result.pa_phone = get_phone_design(patient_result.pa_phone)
        patient_result.pa_cell_phone = get_phone_design(patient_result.pa_cell_phone)
        patient_result.pa_cell_phone_add1 = get_special_phone_design(patient_result.pa_cell_phone_add1)
        patient_result.pa_cell_phone_add2 = get_special_phone_design(patient_result.pa_cell_phone_add2)
        if patient_result.pa_cell_phone_sms:
            patient_result.pa_cell_phone_sms = "#" + patient_result.pa_cell_phone_sms.replace('/', '')


        therapy_result = Therapy.objects.filter(patients_id=patient_helper).order_by('-recipe_date')
        therapy_result_count = Therapy.objects.filter(patients_id=patient_helper, recipe_date__gte='2021-01-01').count()
        process_result_count = 0

        if Patient_Something.objects.filter(patient_id=id).exists():
            patient_something_value = Patient_Something.objects.get(patient_id=id)
        else:
            patient_something_value = ''

        i = 0
        for therapy_result_item in therapy_result:
            x = therapy_result_item.recipe_date
            d1 = datetime.datetime(x.year, x.month, x.day)
            d2 = datetime.datetime(2021, 1, 1)
            if d1 >= d2:
                process_result_count = Process_report.objects.filter(
                    therapy_id=therapy_result_item.id).count() + process_result_count
            therapy_result[i].single = Process_report.objects.filter(therapy_id=therapy_result_item.id).count()
            therapy_report_result = Therapy_report.objects.filter(therapy_id=therapy_result_item.id)
            try:
                therapy_result[i].therapy_start = therapy_report_result[0].therapy_start
                therapy_result[i].therapy_end = therapy_report_result[0].therapy_end
                therapy_result[i].report_date = therapy_report_result[0].report_date
                therapy_result[i].report_id = therapy_report_result[0].id
                therapy_result[i].necessary = therapy_report_result[0].therapy_necessary
            except:
                logger.debug("Try Exception")
            i = i + 1
        logger.info('{:>2}'.format(request.user.id) + ' patient: Patient mit der ID: ' + str(id) + ' aufgerufen')
        return render(request, 'reports/patient.html', {'patient': patient_result,
                                                        'therapy': therapy_result,
                                                        'ps': patient_something_value,
                                                        'therapy_count': therapy_result_count,
                                                        'process_count': process_result_count
                                                        })
    except ObjectDoesNotExist:
        logger.debug('patient: Objekt existiert nicht')
        return redirect('/reports/')



##########################################################################
# Area Patient Sonstiges create and change
##########################################################################
@login_required
def add_pa_something(request):
    if request.method == "POST":
        form = PatientSomethingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_pa_something: Sonstiges mit id: ' + str(
                item.id) + ' angelegt')
            return redirect('/reports/patient/' + str(request.POST.get('patient')))
    else:
        logger.debug('add_pa_something: Formular zur Bearbeitung/Erfassung des Sonstiges-Feld am Patienten')
        patient_result = Patient.objects.get(id=request.GET.get('id'))
        form = PatientSomethingForm(
            initial={'patient': patient_result})
    return render(request, 'reports/pa_something_form.html', {'form': form})

@login_required
def edit_pa_something(request, id=None):
    item = get_object_or_404(Patient_Something, id=id)
    form = PatientSomethingForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_pa_something: Sonstiges ändern mit ID: ' + str(id))
        return redirect('/reports/patient/' + str(item.patient_id))
    logger.debug('edit_pa_something: Sonstige Form aufgerufen für ID: ' + id)
    return render(request, 'reports/pa_something_form.html', {'form': form})


##########################################################################
# Area Initial Assessment create and change
##########################################################################
@login_required
def add_ia(request):
    if request.method == "POST":
        form = InitialAssessmentForm(request.POST)
        if form.is_valid():
            InitialAssessment_item = form.save(commit=False)
            InitialAssessment_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_ia: Erstbefund mit id: ' + str(
                InitialAssessment_item.id) + ' angelegt')
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=1')
    else:
        logger.debug('add_ia: Formular zur Bearbeitung/Erfassung des Erstbefunds')
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = InitialAssessmentForm(
            initial={'therapy': therapy_result})
    return render(request, 'reports/ia_form.html', {'form': form})

@login_required
def edit_ia(request, id=None):
    item = get_object_or_404(InitialAssessment, id=id)
    form = InitialAssessmentForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_ia: Erstbefund ändern mit ID: ' + str(id))
        return redirect('/reports/therapy/' + str(item.therapy_id) + '/?window=1')
    logger.debug('edit_ia: Erstbefund Form angerufen mit ID: ' + id)
    return render(request, 'reports/ia_form.html', {'form': form})


##########################################################################
# Area Therapy Sonstiges create and change
##########################################################################
@login_required
def add_therapy_something(request):
    if request.method == "POST":
        form = TherapySomethingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_therapy_something: Sonstiges mit id: ' + str(
                item.id) + ' angelegt')
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=2')
    else:
        logger.debug('add_therapy_something: Formular zur Bearbeitung/Erfassung des Sonstiges-Feld')
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = TherapySomethingForm(
            initial={'therapy': therapy_result})
    return render(request, 'reports/something_form.html', {'form': form})

@login_required
def edit_therapy_something(request, id=None):
    item = get_object_or_404(Therapy_Something, id=id)
    form = TherapySomethingForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_therapy_something: Sonstiges ändern mit ID: ' + str(id))
        return redirect('/reports/therapy/' + str(item.therapy_id) + '/?window=2')
    logger.debug('edit_therapy_something: Sonstige Form aufgerufen für ID: ' + id)
    return render(request, 'reports/something_form.html', {'form': form})


##########################################################################
# Area Therapy create and change
##########################################################################

@login_required
def add_therapy(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    if request.method == "POST":
        form = TherapyForm(request.POST)
        patient_result = Patient.objects.get(id=request.POST.get('patients'))
        if form.is_valid():
            therapy_item = form.save(commit=False)
            therapy_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_therapy: Rezept für Patient mit ID: ' + str(
                patient_result.id) + ' angelegt')
            return redirect('/reports/patient/' + str(patient_result.id) + '/')
        else:
            logger.info('Dates not valid')
    else:
        logger.info('add_therapy: Formular aufgerufen um eine Rezept anzulegen')
        form = TherapyForm(initial={'patients': request.GET.get('id')})
        patient_result = Patient.objects.get(id=request.GET.get('id'))
    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': patient_result})


@login_required
def edit_therapy(request, id=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    item = get_object_or_404(Therapy, id=id)
    form = TherapyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_therapy: Rezept mit der ID:' + str(item.id) + ' geändert')
        return redirect('/reports/therapy/' + str(item.id) + '/')
    logger.debug('edit_therapy: Rezeptformular des Patienten mit der ID: ' + str(item.id) + ' zwecks Änderung aufgerufen')
    doctor_value = Doctor.objects.get(id=item.therapy_doctor.id)
    data = {'id': item.id,
            'recipe_date': item.recipe_date,
            'therapy_regulation_amount': item.therapy_regulation_amount,
            'therapy_duration': item.therapy_duration,
            'therapy_frequence': item.therapy_frequence,
            'therapy_rid_of': item.therapy_rid_of,
            'therapy_report_no_yes': item.therapy_report_no_yes,
            'therapy_homevisit_no_yes': item.therapy_homevisit_no_yes,
            'therapy_indication_key': item.therapy_indication_key,
            'therapy_icd_cod': item.therapy_icd_cod,
            'therapy_icd_cod_2': item.therapy_icd_cod_2,
            'therapy_doctor': doctor_value,
            'patients': item.patients,
            'therapists': item.therapists,
            'first_diagnostic_no_yes': item.first_diagnostic_no_yes,
            'need_diagnostic_no_yes': item.need_diagnostic_no_yes,
            'continue_diagnostic_no_yes': item.continue_diagnostic_no_yes,
            'diagnostic_group': item.diagnostic_group}

    form = TherapyForm(data)
    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': item.patients})


@login_required
def therapy(request, id=id):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    therapy_result = Therapy.objects.get(id=id)
    patient_value = Patient.objects.get(id=str((therapy_result.patients_id)))
    process_report_value = Process_report.objects.filter(therapy_id=id).order_by('-process_treatment')
    process_report_value.countvalue = Process_report.objects.filter(therapy_id=id).count()
    if Therapy_report.objects.filter(therapy_id=id).exists():
        therapy_report_value = Therapy_report.objects.get(therapy_id=id)
    else:
        therapy_report_value = ''
    if InitialAssessment.objects.filter(therapy_id=id).exists():
        ia_value = InitialAssessment.objects.get(therapy_id=id)
    else:
        ia_value = ''
    if Therapy_Something.objects.filter(therapy_id=id).exists():
        therapy_something_value = Therapy_Something.objects.get(therapy_id=id)
    else:
        therapy_something_value = ''
    logger.info('{:>2}'.format(request.user.id) + ' therapy: Rezept mit der ID: ' + str(id) + ' aufgerufen')
    return render(request, 'reports/therapy.html', {'therapy': therapy_result,
                                                    'patient': patient_value,
                                                    'ia': ia_value,
                                                    'ts': therapy_something_value,
                                                    'therapy_report': therapy_report_value,
                                                    'process_report': process_report_value})


##########################################################################
# Area Process Report (in German: Verlaufsprotokol)
##########################################################################

@login_required
def add_process_report(request):
    if request.method == "POST":
        form = ProcessReportForm(request.POST)
        if form.is_valid():
            therapy_report_item = form.save(commit=False)
            therapy_report_item.save()
            logger.info(
                '{:>2}'.format(request.user.id) + ' add_process_report: Verlaufsprotokoll gespeichert mit ID: ' + str(
                    request.POST.get('therapy')))
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=3')
    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = ProcessReportForm(
            initial={'process_treatment': Process_report.objects.filter(therapy_id=request.GET.get('id')).count() + 1,
                     'therapy': therapy_result})
        logger.debug('add_process_report: Verlaufsprotokoll anlegen mit ID: ' + request.GET.get('id'))
        return render(request, 'reports/process_report_form.html', {'form': form})


@login_required
def edit_process_report(request, id=None):
    item = get_object_or_404(Process_report, id=id)
    form = ProcessReportForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(
            '{:>2}'.format(request.user.id) + ' edit_process_report: Verlaufsprotokoll ändern mit ID: ' + str(item.id))
        return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=3')
    logger.info('{:>2}'.format(request.user.id) + ' edit_process_report: Verlaufsprotokoll anlegen mit ID: ' + id)
    return render(request, 'reports/process_report_form.html', {'form': form})


@login_required
def delete_process_report(request, id=None):
    item = get_object_or_404(Process_report, id=id)
    therapy_id = item.therapy_id
    if item:
        item.delete()
        return redirect('/reports/therapy/' + str(therapy_id) + '/?window=3')
    else:
        return redirect('/reports/')


@login_required
def process_report(request, id=id):
    process_report = Process_report.objects.get(id=id)
    logger.debug('process_report: Verlaufsprotokoll mit ID: ' + id + ' anzeigen')
    return render(request, 'reports/process_report.html', {'process_report': process_report})


@login_required
def show_process_report(request):
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleN.fontSize = 8
    styleNC = styles['Normal']
    styleNC.alignment = TA_JUSTIFY
    styleNC.fontSize = 8
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 8

    def coord(x, y, height, unit=1):
        x, y = x * unit, height - y * unit
        return x, y

    therapy_start_value = ''
    therapy_end_value = ''
    id = request.GET.get('id')
    logger.info('{:>2}'.format(request.user.id) + ' show_process_report: Verlaufsprotokoll mit ID: ' + id + ' gedruckt')
    therapy_value = Therapy.objects.get(id=id)
    pa_first_name = Therapy.objects.get(id=id).patients.pa_first_name
    pa_last_name = Therapy.objects.get(id=id).patients.pa_last_name
    if Therapy_report.objects.filter(therapy=id):
        therapy_report_value = Therapy_report.objects.get(therapy=id)
        therapy_start_value = therapy_report_value.therapy_start
        therapy_end_value = therapy_report_value.therapy_end

    process_report_value = Process_report.objects.values_list('process_treatment',
                                                              'process_content',
                                                              'process_exercises',
                                                              'process_results',
                                                              'process_content_2',
                                                              'process_exercises_2',
                                                              'process_results_2',
                                                              'process_content_3',
                                                              'process_exercises_3',
                                                              'process_results_3'
                                                              ).filter(therapy=id)
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont('Helvetica', 18)
    p.drawString(6 * cm, 28 * cm, "Therapieverlaufdokumentation")
    p.setFont('Helvetica', 10)
    p.drawString(1.5 * cm, 27 * cm, "Rezept - Datum: " + str(therapy_value.recipe_date.strftime("%d.%m.%Y")))
    p.drawString(12 * cm, 27 * cm, "Patient: " + pa_last_name + ", " + pa_first_name)
    p.setFont('Helvetica', 10)
    p.drawString(1.5 * cm, 26.5 * cm, "Bericht: ")
    p.drawString(13 * cm, 26.5 * cm, "Behandlung von: ")

    if therapy_start_value != '' and therapy_start_value is not None:
        p.drawString(15.8 * cm, 26.5 * cm, str(therapy_start_value.strftime("%d.%m.%Y")) + " bis: ")
    if therapy_end_value != '' and therapy_end_value is not None:
        p.drawString(18.3 * cm, 26.5 * cm, str(therapy_end_value.strftime("%d.%m.%Y")))
    p.setFont('Helvetica', 8)
    p.drawString(1.5 * cm, 0.5 * cm, "Druckdatum: " + str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M")))

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
        content = str(escape(item[1])).replace('\n', '<br />\n')
        # content = '<font size=8>' + content + '</font>'
        ccontent = Paragraph(((content)), styleN)
        cexercises = Paragraph((escape(item[2])), styleN)
        cresult = Paragraph((escape(item[3])), styleNC)
        data.append([ctreatment, ccontent, cexercises, cresult])
        if item[4]:
            ctreatment = ''
            content = str(escape(item[4])).replace('\n', '<br />\n')
            ccontent = Paragraph(((content)), styleN)
            cexercises = Paragraph((escape(item[5])), styleN)
            cresult = Paragraph((escape(item[6])), styleNC)
            data.append([ctreatment, ccontent, cexercises, cresult])
        if item[7]:
            ctreatment = ''
            content = str(escape(item[7])).replace('\n', '<br />\n')
            ccontent = Paragraph(((content)), styleN)
            cexercises = Paragraph((escape(item[8])), styleN)
            cresult = Paragraph((escape(item[9])), styleNC)
            data.append([ctreatment, ccontent, cexercises, cresult])


    # create table
    table = Table(data, colWidths=[1.5 * cm, 10 * cm, 5.5 * cm,
                                   1.7 * cm])

    table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP')
                               ]))
    w, h = table.wrap(width, height)
    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(1.5, 3.5, height - h, cm))

    # Close the PDF object cleanly, and we're done.
    #p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    file_name = pa_last_name + "_" + pa_first_name + "_" + str(therapy_value.recipe_date) + ".pdf"
    return FileResponse(buffer, as_attachment=True, filename=file_name)

@login_required
def show_process_report2(request):
    therapy_start_value = ''
    therapy_end_value = ''
    id = request.GET.get('id')
    logger.info('{:>2}'.format(request.user.id) + ' show_process_report2: Verlaufsreport mit ID: ' + id + ' gedruckt')
    therapy_value = Therapy.objects.get(id=id)
    therapy_value.pa_first_name = Therapy.objects.get(id=id).patients.pa_first_name
    therapy_value.pa_last_name = Therapy.objects.get(id=id).patients.pa_last_name
    therapy_value.print_date = datetime.datetime.now()
    if Therapy_report.objects.filter(therapy=id):
        therapy_report_value = Therapy_report.objects.get(therapy=id)
        therapy_value.therapy_start_value = therapy_report_value.therapy_start
        therapy_value.therapy_end_value = therapy_report_value.therapy_end

    #process_report_value = Process_report.objects.values_list('process_treatment',
    #                                                          'process_content',
    #                                                          'process_exercises',
    #                                                          'process_results',
    #                                                          'process_content_2',
    #                                                          'process_exercises_2',
    #                                                          'process_results_2',
    #                                                          'process_content_3',
    #                                                          'process_exercises_3',
    #                                                          'process_results_3'
    #                                                          ).filter(therapy=id)

    process_report_value = Process_report.objects.filter(therapy=id)

    process_report_value.static_root = settings.STATIC_ROOT

    filename = "Verlauf_" + therapy_value.pa_last_name + "_" + therapy_value.pa_first_name + "_" + str(therapy_value.recipe_date) + ".pdf"

    html_string = render_to_string('pdf_templates/process_report.html', {'therapy': therapy_value,
                                                                         'process': process_report_value
                                                                         })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/reports/process_report.css')])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    return response
##########################################################################
# Area Therapyreport (in German: Therapiebericht)
##########################################################################

@login_required
def add_therapy_report(request):
    if request.method == "POST":
        form = TherapyReportForm(request.POST)
        if form.is_valid():
            therapy_report_item = form.save(commit=False)
            therapy_report_item.save()
            logger.info(
                '{:>2}'.format(request.user.id) + ' add_therapy_report: Therapiebericht gespeichert mit ID: ' + str(
                    request.POST.get('therapy')))
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=4')
        else:
            return render(request, 'reports/therapy_report_form.html', {'form': form})

    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = TherapyReportForm(
            initial={'therapy': therapy_result})
        logger.info('{:>2}'.format(request.user.id) + ' add_therapy_report: Therapiebericht gespeichert mit ID: ' + str(
            request.POST.get('therapy')))
        return render(request, 'reports/therapy_report_form.html', {'form': form})


@login_required
def edit_therapy_report(request, id=None):
    item = get_object_or_404(Therapy_report, id=id)
    form = TherapyReportForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_therapy_report: Therapiebericht ändern mit ID: ' + str(id))
        return redirect('/reports/therapy/' + str(item.therapy_id) + '/?window=4')
    logger.debug('edit_therapy_report: Therapybericht anlegen mit ID: ' + id)
    return render(request, 'reports/therapy_report_form.html', {'form': form})


@login_required
def therapy_report(request, id=id):
    therapy_report = Therapy_report.objects.get(id=id)
    logger.info('{:>2}'.format(request.user.id) + ' therapy_report: Therapiebericht mit ID: ' + id + ' anzeigen')
    return render(request, 'reports/therapy_report.html', {'therapy_report': therapy_report})


@login_required
def show_therapy_report(request):
    id = request.GET.get('id')
    logger.info('{:>2}'.format(request.user.id) + ' show_therapy_report: Therapiebericht mit ID: ' + id + ' gedruckt')
    therapy_result = Therapy.objects.get(id=request.GET.get('id'))
    result = Therapy_report.objects.get(therapy=request.GET.get('id'))
    doctor_result = Doctor.objects.get(id=therapy_result.therapy_doctor_id)
    result.pa_first_name = Therapy.objects.get(id=id).patients.pa_first_name
    result.pa_last_name = Therapy.objects.get(id=id).patients.pa_last_name
    result.pa_date_of_birth = Therapy.objects.get(id=id).patients.pa_date_of_birth
    result.recipe_date = Therapy.objects.get(id=id).recipe_date
    result.process_count = Process_report.objects.filter(therapy=id).count()
    result.static_root = settings.STATIC_ROOT

    filename = result.pa_last_name + "_" + result.pa_first_name + "_" + str(result.recipe_date) + ".pdf"

    html_string = render_to_string('pdf_templates/therapy_report.html', {'therapy': therapy_result,
                                                                         'result': result,
                                                                         'doctor': doctor_result
                                                                         })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/reports/therapy_report.css')])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    return response


@login_required
def add_waitlist(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    if request.method == "POST":
        form = WaitlistForm(request.POST)
        if form.is_valid():
            waitlist_item = form.save(commit=False)
            waitlist_item.save()
            logger.info('{:>2}'.format(request.user.id) + ' add_waitlist: Waitlist mit der ID:' + str(
                waitlist_item.id) + ' gespeichert')
            return redirect('/reports/edit/waitlist/' + str(waitlist_item.id) + '/')
        else:
            print('Problems with form')
    else:
        logger.debug('add_waitlist: Formular aufgerufen')
        form = WaitlistForm()
    return render(request, 'reports/waitlist_form.html', {'form': form})


@login_required
def edit_waitlist(request, id=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    item = get_object_or_404(Wait_list, id=id)
    form = WaitlistForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('{:>2}'.format(request.user.id) + ' edit_waitlist: Wait_list mit der ID:' + str(item.id) + ' geändert')
        return redirect('/reports/edit/waitlist/' + str(item.id) + '/')
    logger.debug('edit_waitlist: Wait-list mit der ID: ' + str(id) + ' zwecks Änderung aufgerufen')
    form.id = item.id
    return render(request, 'reports/waitlist_form.html', {'form': form})


@login_required
def waitlist(request, status):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    waitlist = Wait_list.objects.filter(wl_active=status).order_by('wl_call_date')

    for waitlist_item in waitlist:
        waitlist_item.wl_phone = get_phone_design(waitlist_item.wl_phone)
        waitlist_item.wl_cell_phone = get_phone_design(waitlist_item.wl_cell_phone)

    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': status})


@login_required
def copy_waitlist_item(request, id=id):
    #select waitlist object
    waitlist = get_object_or_404(Wait_list, id=id)

    #create patient_object
    Patient.objects.create(pa_first_name=waitlist.wl_first_name,
        pa_last_name=waitlist.wl_last_name,
        pa_street=waitlist.wl_street,
        pa_city=waitlist.wl_city,
        pa_zip_code=waitlist.wl_zip_code,
        pa_phone=waitlist.wl_phone,
        pa_cell_phone=waitlist.wl_cell_phone,
        pa_cell_phone_add1=waitlist.wl_cell_phone_add1,
        pa_cell_phone_add2=waitlist.wl_cell_phone_add2,
        pa_cell_phone_sms=waitlist.wl_cell_phone_sms,
        pa_email=waitlist.wl_email,
        pa_gender=waitlist.wl_gender
    )

    #set status waitlist object to False
    waitlist.wl_active = False
    waitlist.save()

    #Info to Webfrontwend
    waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')
    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})


@login_required
def delete_waitlist_item(request, id=None):
    item = get_object_or_404(Wait_list, id=id)
    if item:
        item.delete()
        waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')
        return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})
    else:
        return redirect('/reports/')


@login_required
def set_waitlist_item_inactive(request, id=None):
    item = get_object_or_404(Wait_list, id=id)
    if item:
        item.wl_active = False
        item.save()
    else:
        logger.info('{:>2}'.format(request.user.id) + ' set_waitlist_item_inactive: Wait_list mit der ID:' + str(item.id) + ' konnte nicht auf inaktive gesetzt werden')
    waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')
    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})


@login_required
def set_waitlist_item_active(request, id=None):
    item = get_object_or_404(Wait_list, id=id)
    if item:
        item.wl_active = True
        item.save()
    else:
        logger.info('{:>2}'.format(request.user.id) + ' set_waitlist_item_active: Wait_list mit der ID:' + str(item.id) + ' konnte nicht auf aktive gesetzt werden')
    waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')
    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})

##########################################################################
# Area Document upload
##########################################################################

@login_required
def upload_document(request):
    if request.method == 'POST':
        item_form = DocumentForm(request.POST, request.FILES)
        patient_result = Patient.objects.get(id=request.POST.get('patient'))
        if item_form.is_valid():
            logger.debug('upload_document: Dokument zum speichern valide')
            item = item_form.save(commit=False)
            item.patient_id = patient_result.id
            item.save()
            logger.debug('upload_document: Dokument gespeichert')
            return redirect('/reports/document/?id=' + str(patient_result.id))
    else:
        logger.debug('upload_document: Formular aufgerufen um Dokumente zu sehen oder hochzuladen')
        form = DocumentForm(initial={'patient': request.GET.get('id')})
        patient_result = Patient.objects.get(id=request.GET.get('id'))
        documents = Document.objects.filter(patient_id=request.GET.get('id')).order_by('-uploaded_at')
    return render(request, 'reports/document_form.html',
                  {'form': form, 'patient': patient_result, 'documents': documents})


IMAGE_FILE_TYPES = ['pdf']


@login_required
def download_document(request):
    if request.method == 'GET':
        file_id = request.GET.get('id')
        logger.debug('download_document: Dokument mit file_id: ' + file_id + ' downloaded')
        file_info = Document.objects.get(id=file_id)
        document_name = file_info.document.name
        document_path = settings.MEDIA_ROOT + '/' + document_name
        response = FileResponse(open(document_path, 'rb'), as_attachment=True)
        return response

    logger.debug('download_document: keine Get-Methode beim Download')
    return redirect('/reports/')


class del_document(DeleteView):
    model = Document
    template_name = 'reports/document_confirm_delete.html'
    context_object_name = 'documents'
    success_url = reverse_lazy('reports:document')

    def post(self, request, *args, **kwargs):
        patient_id = request.POST.get('patient_id')
        file_id = kwargs['pk']
        file_info = Document.objects.get(id=file_id)
        document_name = file_info.document.name
        document_path = settings.MEDIA_ROOT + '/' + document_name
        if os.path.exists(document_path):
            os.remove(document_path)
            file_info.delete()
            logger.debug('del_document: Dokument: ' + document_name + " gelöscht")
        else:
            logger.debug('del_document: Dokument: ' + document_path + " konnte nicht gelöscht werden")

        return HttpResponseRedirect(self.success_url + "?id=" + patient_id)


##########################################################################
# Area Document upload
##########################################################################

@login_required
def upload_document_therapy(request):
    if request.method == 'POST':
        item_form = DocumentTherapyForm(request.POST, request.FILES)
        therapy_result = Therapy.objects.get(id=request.POST.get('therapy'))
        if item_form.is_valid():
            logger.debug('upload_document_therapy: Dokument zum speichern valide')
            item = item_form.save(commit=False)
            item.therapy_id = therapy_result.id
            item.save()
            logger.debug('upload_document_therapy: Dokument gespeichert')
            return redirect('/reports/document_therapy/?id=' + str(therapy_result.id))
    else:
        logger.debug('upload_document_therapy: Formular aufgerufen um Dokumente zu sehen oder hochzuladen')
        form = DocumentTherapyForm(initial={'therapy': request.GET.get('id')})
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        documents = Document_therapy.objects.filter(therapy_id=request.GET.get('id')).order_by('-uploaded_at')
    return render(request, 'reports/document_therapy_form.html',
                  {'form': form, 'therapy': therapy_result, 'documents': documents})


IMAGE_FILE_TYPES = ['pdf']


@login_required
def download_document_therapy(request):
    if request.method == 'GET':
        file_id = request.GET.get('id')
        file_info = Document_therapy.objects.get(id=file_id)
        document_name = file_info.document.name
        document_path = settings.MEDIA_ROOT + '/' + document_name
        response = FileResponse(open(document_path, 'rb'), as_attachment=True)
        return response

    return redirect('/reports/')


class del_document_therapy(DeleteView):
    model = Document_therapy
    template_name = 'reports/document_therapy_confirm_delete.html'
    context_object_name = 'documents'
    success_url = reverse_lazy('reports:document_therapy')

    def post(self, request, *args, **kwargs):
        therapy_id = request.POST.get('therapy_id')
        file_id = kwargs['pk']
        file_info = Document_therapy.objects.get(id=file_id)
        document_name = file_info.document.name
        document_path = settings.MEDIA_ROOT + '/' + document_name
        if os.path.exists(document_path):
            os.remove(document_path)
            file_info.delete()
            logger.debug('del_document_therapy: Dokument: ' + document_name + " gelöscht")
        else:
            logger.debug('del_document_therapy: Dokument: ' + document_path + " konnte nicht gelöscht werden")

        return HttpResponseRedirect(self.success_url + "?id=" + therapy_id)


# **************************************************************************************************

@login_required
def getSessionTimer(request):
    sessionTimer = request.session.get_expiry_date()
    sessionTimer = sessionTimer.isoformat()
    context = {'getSessionTimer': str(sessionTimer)}
    logger.info('{:>2}'.format(request.user.id) + " getSessionTimer: " + str(sessionTimer))

    return render(request, 'getSessionTimer.html', {'form': context})

class openContext:
    pass

@login_required
def getOpenReports(request, context=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    therapist_value = Therapist.objects.filter(tp_user_logopakt=str(request.user))
    if therapist_value:
        therapy_list = Therapy.objects.filter(therapists=therapist_value[0].id,
                                              therapy_report_no_yes=True).order_by('recipe_date')
    else:
        therapy_list = Therapy.objects.filter(therapy_report_no_yes=True).order_by('recipe_date')
    reports_list = []
    for tp_item in therapy_list:
        report_date_value = ''
        process_report_value = Process_report.objects.filter(therapy=tp_item.id)
        process_report_value_count = process_report_value.count()
        tp_item.prvc = process_report_value_count
        quotient = process_report_value_count / int(tp_item.therapy_regulation_amount)
        if quotient > 0.6:
            therapy_report_result = Therapy_report.objects.filter(therapy_id=tp_item.id)
            try:
                report_date_value = therapy_report_result[0].report_date
            except:
                logger.debug("Try Exception")

            if not report_date_value:
                patient_value = Patient.objects.filter(id=tp_item.patients.id)
                tp_item.pa_last_name = patient_value[0].pa_last_name
                tp_item.pa_first_name = patient_value[0].pa_first_name
                reports_list.append(tp_item)

    #Ermittlung der Therapieberichte bei den "Pause" ausgewählt ist
    if request.user.groups.filter(name='Leitung').exists():
        therapybreak_count = Therapy_report.objects.\
            select_related('therapy__patients').\
            filter(therapy_break_internal=True,
                    therapy_end__lte=datetime.date.today() + datetime.timedelta(days=-21),
                    therapy__patients__pa_active_no_yes=True).count()
    else:
        therapybreak_count = Therapy_report.objects.\
            select_related('therapy__patients').\
            filter(therapy_break_internal=True,
                    therapy_end__lte=datetime.date.today() + datetime.timedelta(days=-21),
                    therapy__therapists__tp_user_logopakt=str(request.user),
                    therapy__patients__pa_active_no_yes=True).count()


    openReports = len(reports_list)

    #context = {'getOpenReports': str(openReports)}
    openContext.getOpenReports = str(openReports)
    openContext.therapybreak_count = str(therapybreak_count)
    logger.info('{:>2}'.format(request.user.id) + ' getOpenReports aufgerufen')

    return render(request, 'getOpenReports.html', {'form': openContext})


def get_phone_design(data):
    charvalue = ''
    charvalue2 = ''

    if data:
        data = data.replace(' ', '')
        data = data.rsplit("/")
        if len(data[1]) % 2:
            for char in data[1]:
                charvalue = charvalue + char
                charvalue2 = charvalue2 + char
                if len(charvalue2) % 2:
                    charvalue = charvalue + " "
        else:
            for char in data[1]:
                charvalue = charvalue + char
                charvalue2 = charvalue2 + char
                if not len(charvalue2) % 2:
                    charvalue = charvalue + " "

        return data[0] + " / " + charvalue


def get_special_phone_design(data):
    charvalue = ''
    charvalue2 = ''
    if data:
        data = data.rsplit("/")
        rightdata = data[1].rsplit("(")
        data[0] = data[0].replace(' ', '')
        rightdata[0] = rightdata[0].replace(' ', '')

        if len(rightdata[0]) % 2:  # rightdata[0] ist die Rufnummer
            for char in rightdata[0]:
                charvalue = charvalue + char
                charvalue2 = charvalue2 + char
                if len(charvalue2) % 2:
                    charvalue = charvalue + " "
        else:
            for char in rightdata[0]:
                charvalue = charvalue + char
                charvalue2 = charvalue2 + char
                if not len(charvalue2) % 2:
                    charvalue = charvalue + " "

        data = data[0] + " / " + charvalue + "  (" + rightdata[1]
        return data


@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    logger.info('{:>2}'.format(user.id) + " " + format(user) + ' eingeloggt')
    try:
        Login_Failed.objects.filter(user_name=user).delete()
        logger.debug("Userdaten von " + format(user) + " in failed_login gelöscht")
    except:
        logger.debug("User not found")

@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    logger.info(f"Post_logout: User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; {request.session.get_expiry_date()}; {datetime.datetime.utcnow()}; Logout")

    try:
        logger.info('{:>2}'.format(user.id) + ' ausgeloggt')
    except:
        logger.info('User ausgeloggt')

@receiver(user_login_failed)
def post_login_failed(sender, credentials, request, **kwargs):
    logger.debug("%s Authentication failure for user %s" % (request.META['REMOTE_ADDR'], credentials['username']))
    user_local = ''
    try:
        user_local = User.objects.get(username=credentials['username'])
        logger.debug('User bekannt: speichern des Users')
    except:
        logger.debug('User unbekannt: speichern des Users')

    if user_local:
        if X_FORWARD:
            b = Login_Failed(ipaddress=request.META['HTTP_X_FORWARDED_FOR'], user_name=credentials['username'])
        else:
            b = Login_Failed(ipaddress=request.META['REMOTE_ADDR'], user_name=credentials['username'])

        b.save()
        failed_count = Login_Failed.objects.filter(user_name=credentials['username'])
        x = failed_count.count()
        if x > 5:
            logger.debug('Fehlversuche: ' + credentials['username'] + ": " + str(x))
            user_local.request_status = 'A'
            user_local.is_active = False
            user_local.save()
            send_mail(
                subject='ACHTUNG: Anmeldefehlversuche logoPAkt!!!',
                message='User: ' + credentials['username'] + ' hat sich mehr als ' + str(x) + 'x mit falschem Passwort eingeloggt und wurde deaktiviert',
                from_email='logopaedieklein.raspberry@gmail.com',
                recipient_list=['norbert.krings@gmail.com', ],
                fail_silently=False,
            )
    else:
        if X_FORWARD:
            b = Login_Failed(ipaddress=request.META['HTTP_X_FORWARDED_FOR'])
        else:
            b = Login_Failed(ipaddress=request.META['REMOTE_ADDR'])

        b.save()
        failed_count = Login_Failed.objects.filter(ipaddress=request.META['REMOTE_ADDR'], user_name='')
        x = failed_count.count()
        if x > 5:
            logger.info('Fehlversuche: ' + request.META['REMOTE_ADDR'] + ": " + str(x))
            send_mail(
                subject='ACHTUNG: Anmeldefehlversuche logoPAkt!!!',
                message='IP-Adresse: ' + request.META['REMOTE_ADDR'] + ' hat sich mehr als ' + str(x) + 'x mit falschem Benutzernamen eingeloggt',
                from_email='logopaedieklein.raspberry@gmail.com',
                recipient_list=['norbert.krings@gmail.com', ],
                fail_silently=False,
            )


# **************************************************************************************************

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
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
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': BASE_DIR + '/logopaedie.log',
            'maxBytes': 1024*1024*1,
            'backupCount': 10,
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'reports': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
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
