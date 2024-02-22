import io
import os
import logging
import datetime
import locale
# import json
# import asyncio

#from datetime import date
#from datetime import datetime
from html import escape
from dateutil.parser import parse
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.http import FileResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView
from django.conf import settings
from django.views import generic
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, F
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.serializers import serialize
from email.mime.image import MIMEImage
from django.utils import timezone
from weasyprint import HTML, CSS

from logopaedie.settings import BASE_DIR, X_FORWARD, time_green_value, time_orange_value, time_red_value

from .forms import IndexForm, PatientForm, TherapyForm, ProcessReportForm, TherapyReportForm, DoctorForm, \
    TherapistForm, SearchDoctorForm, SearchTherapistForm, InitialAssessmentForm, DocumentForm, TherapySomethingForm, \
    DocumentTherapyForm, PatientSomethingForm, Diagnostic_groupForm, SearchDiagnostic_groupForm, \
    WaitlistForm

from .models import Patient, Therapy, Process_report, Therapy_report, Doctor, Therapist, InitialAssessment, Document, \
    Therapy_Something, Document_therapy, Patient_Something, Login_Failed, Diagnostic_group, Wait_list, Shortcuts, \
    Login_User_Agent

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")


##########################################################################
# Area start and patient search
##########################################################################
@login_required
def index(request):
    logger.debug(f"User-ID: {request.user.id}; Indexseite wurde geladen")
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    form = IndexForm()
    return render(request, 'reports/index.html', {'form': form})


def impressum(request):
    logger.debug(f"User-ID: {request.user.id}; Impressumseite aufgerufen")
    return render(request, 'reports/impressum.html')


class PatientView(generic.ListView):
    model = Patient
    template_name = 'reports/patients.html'
    context_object_name = 'patients_list'
    logger.debug(f" Patientenliste geladen")

    def get_queryset(self):
        return Patient.objects.all()


##########################################################################
# open Reports
##########################################################################
@permission_required('reports.view_patient')
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
                logger.debug(f"User-ID: {request.user.id}; Try Exception")

            if not report_date_value:
                patient_value = Patient.objects.filter(id=tp_item.patients.id)
                tp_item.pa_last_name = patient_value[0].pa_last_name
                tp_item.pa_first_name = patient_value[0].pa_first_name
                reports_list.append(tp_item)
        logger.debug(f"User-ID: {request.user.id}; "
                     f"verordnet: {str(tp_item.therapy_regulation_amount)}; "
                     f"Therapien: {str(process_report_value_count)}; "
                     f"Quotient: {str(quotient)}; "
                     f"report_date_value: {str(report_date_value)}")

    logger.debug(f"User-ID: {request.user.id}; Open_Reports wurde geladen")
    return render(request, 'reports/open_reports.html', {'reports': reports_list})


##########################################################################
# therapy_breaks_internal
##########################################################################
@permission_required('reports.view_patient')
def therapy_breaks(request):
    if request.user.groups.filter(name='Leitung').exists():
        therapy_reports = Therapy_report.objects. \
            select_related('therapy__patients'). \
            select_related('therapy__therapists'). \
            filter(therapy_break_internal=True,
                   therapy_end__lte=datetime.date.today() + datetime.timedelta(days=time_green_value),
                   therapy__patients__pa_active_no_yes=True).order_by('therapy_end')
    else:
        therapy_reports = Therapy_report.objects. \
            select_related('therapy__patients'). \
            select_related('therapy__therapists'). \
            filter(therapy_break_internal=True,
                   therapy_end__lte=datetime.date.today() + datetime.timedelta(days=time_green_value),
                   therapy__therapists__tp_user_logopakt=str(request.user),
                   therapy__patients__pa_active_no_yes=True).order_by('therapy_end')

    time_green = datetime.datetime.now() + datetime.timedelta(days=time_green_value)
    time_orange = datetime.datetime.now() + datetime.timedelta(days=time_orange_value)
    time_red = datetime.datetime.now() + datetime.timedelta(days=time_red_value)
    # print(f"grün: {time_green}; orange: {time_orange}; red: {time_red}")
    logger.debug(f"User-ID: {request.user.id}; Open_Reports wurde geladen")
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
@permission_required('reports.add_doctor')
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_doctor: 'doc{str(item.id)}';"
                        f"[ doctor_name1: {str(item.doctor_name1)},"
                        f"doctor_name2: {str(item.doctor_name2)},"
                        f"doctor_name3: {str(item.doctor_name3)},"
                        f"doctor_street: {str(item.doctor_street)},"
                        f"doctor_zip_code: {str(item.doctor_zip_code)},"
                        f"doctor_city: {str(item.doctor_city)},"
                        f"doctor_lanr: {str(item.doctor_lanr)} ]")

            return redirect('/reports/doctor/' + str(item.id) + '/')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_doctor: Formular zur Bearbeitung/Erfassung der Arztdaten")
        form = DoctorForm()
    return render(request, 'reports/doctor_form.html', {'form': form})


@permission_required('reports.view_doctor')
def search_doctor_start(request):
    logger.debug(f"User-ID: {request.user.id}; search_doctor_start: Suchmaske Arzt geladen")
    form = SearchDoctorForm()
    return render(request, 'reports/doctor_search.html', {'form': form})


@permission_required('reports.view_doctor')
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
                logger.debug(f"User-ID: {request.user.id}; "
                             f"search_doctor: mehr als einen Arzt gefunden mit dem Suchbegriff: {name1}")
                return render(request, 'reports/doctors.html', {'doctors_list': doctors_list})
            elif len(doctors_list) == 1:
                logger.debug(f"User-ID: {request.user.id}; search_doctor: Arzt gefunden mit dem Suchbegriff: {name1}")
                return redirect('/reports/doctor/' + str(doctors_list[0].id) + '/')
            else:
                logger.debug(f"User-ID: {request.user.id}; search_doctor: Keinen Arzt gefunden "
                             f"mit dem Suchbegriff: {name1}")
                return render(request, 'reports/doctor_search.html', {'form': form})
        elif lanr != "":
            doctors_list = Doctor.objects.filter(doctor_lanr=lanr)
            if len(doctors_list) == 1:
                logger.debug(f"User-ID: {request.user.id}; search_doctor: Arzt gefunden mit dem Suchbegriff: {lanr}")
                return redirect('/reports/doctor/' + str(doctors_list[0].id) + '/')
            else:
                logger.debug(f"User-ID: {request.user.id}; search_doctor: Keinen Arzt gefunden "
                             f"mit dem Suchbegriff: {lanr}")
                return render(request, 'reports/doctor_search.html', {'form': form})
        else:
            logger.debug(f"User-ID: {request.user.id}; search_doctor: Keinen Suchbegriff eingegeben")
            return render(request, 'reports/doctor_search.html', {'form': form})
    else:
        logger.debug(f"User-ID: {request.user.id}; search_doctor: Keinen Suchbegriff eingegeben")
        return render(request, 'reports/doctor_search.html')


@permission_required('reports.change_doctor')
def edit_doctor(request, id=None):
    item = get_object_or_404(Doctor, id=id)
    form = DoctorForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_doctor: 'doc{str(item.id)}';"
                    f"[ doctor_name1: {str(item.doctor_name1)},"
                    f"doctor_name2: {str(item.doctor_name2)},"
                    f"doctor_name3: {str(item.doctor_name3)},"
                    f"doctor_street: {str(item.doctor_street)},"
                    f"doctor_zip_code: {str(item.doctor_zip_code)},"
                    f"doctor_city: {str(item.doctor_city)},"
                    f"doctor_lanr: {str(item.doctor_lanr)} ]")

        return redirect('/reports/doctor/' + str(item.id) + '/')
    logger.debug(f"User-ID: {request.user.id}; edit_doctor: Bearbeitungsformular aufgerufen ID: {id}")
    form.id = item.id
    return render(request, 'reports/doctor_form.html', {'form': form})


@permission_required('reports.view_doctor')
def doctor(request, id=id):
    try:
        doctor_result = Doctor.objects.get(id=id)
        logger.debug(f"User-ID: {request.user.id}; doctor: Arzt mit der ID: {id} aufgerufen")
        return render(request, 'reports/doctor.html', {'doctor': doctor_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')


##########################################################################
# Area Therapist create and change
##########################################################################
@permission_required('reports.add_therapist')
def add_therapist(request):
    if request.method == "POST":
        form = TherapistForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_therapist: 'ther{str(item.id)}';"
                        f"[ tp_first_name: {str(item.tp_first_name)},"
                        f"tp_last_name: {str(item.tp_last_name)},"
                        f"tp_initial: {str(item.tp_initial)},"
                        f"tp_user_logopakt: {str(item.tp_user_logopakt)} ]")

            return redirect('/reports/therapist/' + str(item.id) + '/')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_therapist: Formular zur Bearbeitung/Erfassung "
                     f"der Therapistdaten")
        form = TherapistForm()
    return render(request, 'reports/therapist_form.html', {'form': form})


@permission_required('reports.view_therapist')
def search_therapist_start(request):
    logger.debug(f"User-ID: {request.user.id}; Suchmaske Therapeut geladen")
    form = SearchTherapistForm()
    return render(request, 'reports/therapist_search.html', {'form': form})


@permission_required('reports.view_therapist')
def search_therapist(request):
    form = SearchTherapistForm()
    if request.method == 'POST':
        kuerzel = request.POST['tp_initial']
        if kuerzel != "":
            therapists_list = Therapist.objects.filter(tp_initial__icontains=kuerzel)
            if len(therapists_list) > 1:
                logger.debug(f"User-ID: {request.user.id}; search_therapist: mehr als einen Therapeut "
                             f"gefunden mit dem Suchbegriff: {kuerzel}")
                return render(request, 'reports/therapists.html', {'therapists_list': therapists_list})
            elif len(therapists_list) == 1:
                logger.debug(f"User-ID: {request.user.id}; search_therapist: Therpeut gefunden mit dem "
                             f"Suchbegriff: {kuerzel}")
                return redirect('/reports/therapist/' + str(therapists_list[0].id) + '/')
            else:
                logger.debug(f"User-ID: {request.user.id}; search_therapist: Keinen Therapeut gefunden "
                             f"mit dem Suchbegriff: {kuerzel}")
                return render(request, 'reports/therapist_search.html', {'form': form})

        else:
            logger.debug(f"User-ID: {request.user.id}; search_therapist: Keinen Suchbegriff eingegeben")
            return render(request, 'reports/therapist_search.html', {'form': form})
    else:
        logger.debug(f"User-ID: {request.user.id}; search_therapist: Keinen Suchbegriff eingegeben")
        return render(request, 'reports/therapist_search.html', {'form': form})


@permission_required('reports.change_therapist')
def edit_therapist(request, id=None):
    item = get_object_or_404(Therapist, id=id)
    form = TherapistForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_therapist: 'ther{str(item.id)}';"
                    f"[ tp_first_name: {str(item.tp_first_name)},"
                    f"tp_last_name: {str(item.tp_last_name)},"
                    f"tp_initial: {str(item.tp_initial)},"
                    f"tp_user_logopakt: {str(item.tp_user_logopakt)} ]")

        return redirect('/reports/therapist/' + str(item.id) + '/')
    logger.debug(f"User-ID: {request.user.id}; edit_therapist: Bearbeitungsformular aufgerufen ID: {id}")
    form.id = item.id
    return render(request, 'reports/therapist_form.html', {'form': form})


@permission_required('reports.view_therapist')
def therapist(request, id=id):
    try:
        therapist_result = Therapist.objects.get(id=id)
        logger.debug(f"User-ID: {request.user.id}; therapist: Therapeut mit der ID: {id} aufgerufen")
        return render(request, 'reports/therapist.html', {'therapist': therapist_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')


##########################################################################
# Area Diagnostic_group create and change
##########################################################################
@permission_required('reports.add_diagnostic_group')
def add_diagnostic_group(request):
    if request.method == "POST":
        form = Diagnostic_groupForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_diagnostic_group: 'diag{str(item.id)}';"
                        f"[ diagnostic_key: {str(item.diagnostic_key)},"
                        f"diagnostic_description: {str(item.diagnostic_description)},"
                        f"diagnostic_max_therapy: {str(item.diagnostic_max_therapy)} ]")

            return redirect('/reports/diagnostic_group/' + str(item.id) + '/')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_diagnostic_group: Formular zur Bearbeitung/Erfassung "
                     f"der Diagnosedaten")
        form = Diagnostic_groupForm()
    return render(request, 'reports/diagnostic_group_form.html', {'form': form})


@permission_required('reports.view_diagnostic_group')
def search_diagnostic_group_start(request):
    logger.debug(f"User-ID: {request.user.id}; Suchmaske Diagnosegruppe geladen")
    form = SearchDiagnostic_groupForm()
    return render(request, 'reports/diagnostic_group_search.html', {'form': form})


@permission_required('reports.view_diagnostic_group')
def search_diagnostic_group(request):
    form = SearchDiagnostic_groupForm()
    if request.method == 'POST':
        diagnostic_key = request.POST['diagnostic_key']
        if diagnostic_key != "":
            diagnostic_group_list = Diagnostic_group.objects.filter(diagnostic_key__istartswith=diagnostic_key)

            if len(diagnostic_group_list) > 1:
                logger.debug(f"User-ID: {request.user.id}; search_diagnostic_group: mehr als eine "
                             f"Diagnostic gefunden mit dem Suchbegriff: {diagnostic_key}")
                return render(request, 'reports/diagnostic_groups.html',
                              {'diagnostic_group_list': diagnostic_group_list})
            elif len(diagnostic_group_list) == 1:
                logger.debug(f"User-ID: {request.user.id}; search_diagnostic_group: Diagnosticgruppe gefunden "
                             f"mit dem Suchbegriff: {diagnostic_key}")
                return redirect('/reports/diagnostic_group/' + str(diagnostic_group_list[0].id) + '/')
            else:
                logger.debug(f"User-ID: {request.user.id}; search_diagnostic_group: Keine Diagnosticgruppe "
                             f"gefunden mit dem Suchbegriff: {diagnostic_key}")
                return render(request, 'reports/diagnostic_group_search.html', {'form': form})
        else:
            logger.debug(f"User-ID: {request.user.id}; search_diagnostic_group: Keinen Suchbegriff eingegeben")
            return render(request, 'reports/diagnostic_group_search.html', {'form': form})
    else:
        logger.debug(f"User-ID: {request.user.id}; search_diagnostic_group: Keinen Suchbegriff eingegeben")
        return render(request, 'reports/diagnostic_group_search.html')


@permission_required('reports.change_diagnostic_group')
def edit_diagnostic_group(request, id=None):
    item = get_object_or_404(Diagnostic_group, id=id)
    form = Diagnostic_groupForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_diagnostic_group: 'diag{str(item.id)}';"
                    f"[ diagnostic_key: {str(item.diagnostic_key)},"
                    f"diagnostic_description: {str(item.diagnostic_description)},"
                    f"diagnostic_max_therapy: {str(item.diagnostic_max_therapy)} ]")

        return redirect('/reports/diagnostic_group/' + str(item.id) + '/')
    logger.debug(f"User-ID: {request.user.id}; edit_diagnostic_group: Bearbeitungsformular aufgerufen ID: {id}")
    form.id = item.id
    return render(request, 'reports/diagnostic_group_form.html', {'form': form})


@permission_required('reports.view_diagnostic_group')
def diagnostic_group(request, id=id):
    try:
        diagnostic_group_result = Diagnostic_group.objects.get(id=id)
        logger.debug(f"User-ID: {request.user.id}; diagnostic_group: Diagnosegruppe mit der ID: {id} aufgerufen")
        return render(request, 'reports/diagnostic_group.html', {'diagnostic_group': diagnostic_group_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')


##########################################################################
# Area Patient search, create and change
##########################################################################
@permission_required('reports.view_patient')
def search_patient(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")

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
            logger.debug(f"User-ID: {request.user.id}; active: {str(active)}")
            data = request.POST['phone']
            if data:
                phone = data.replace(' ', '')

            data = request.POST['cell_phone']
            if data:
                cell_phone = data.replace(' ', '')

            if last_name != "":
                if active is True or active is False:
                    patients_list = Patient.objects.filter(pa_last_name__istartswith=last_name,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_last_name__istartswith=last_name).order_by('pa_last_name',
                                                                                                         'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Mehrere Patienten mit dem Namen: "
                                 f"{last_name} gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Patient mit dem Suchbegriff: "
                                 f"{last_name} gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Kein Patient mit dem Nachnamen: "
                                 f"{last_name} gefunden")
                    return redirect('/reports/')

            elif first_name != "":
                if active is True or active is False:
                    patients_list = Patient.objects.filter(pa_first_name__istartswith=first_name,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_first_name__istartswith=first_name).order_by(
                        'pa_last_name', 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Mehrere Patienten mit dem Vornamen: "
                                 f"{first_name} gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Patient mit dem Suchbegriff: "
                                 f"{first_name} gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Kein Patient mit dem Vornamen:"
                                 f" {first_name} gefunden")
                    return redirect('/reports/')

            elif date_of_birth != "":
                if active is True or active is False:
                    patients_list = Patient.objects.filter(pa_date_of_birth=parse(date_of_birth, dayfirst=True),
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(
                        pa_date_of_birth=parse(date_of_birth, dayfirst=True)).order_by('pa_last_name', 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Mehrere Patienten mit dem Geburtsdatum "
                                 f"{date_of_birth} gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Patient mit dem Geburtsdatum: "
                                 f"{date_of_birth}  gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Kein Patient mit dem Geburtsdatum: "
                                 f"{last_name} gefunden")
                    return redirect('/reports/')

            elif phone != "":
                if active is True or active is False:
                    patients_list = Patient.objects.filter(pa_phone__istartswith=phone,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_phone__istartswith=phone).order_by('pa_last_name',
                                                                                                 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Mehrere Patienten mit der "
                                 f"Telefonnummer {phone} gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Patient mit der "
                                 f"Telefonnummer: {phone} gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Kein Patient mit der "
                                 f"Telefonnummer: {phone} gefunden")
                    return redirect('/reports/')

            elif cell_phone != "":
                if active is True or active is False:
                    patients_list = Patient.objects.filter(pa_cell_phone__istartswith=cell_phone,
                                                           pa_active_no_yes=active).order_by('pa_last_name',
                                                                                             'pa_first_name')
                else:
                    patients_list = Patient.objects.filter(pa_cell_phone__istartswith=cell_phone).order_by(
                        'pa_last_name', 'pa_first_name')

                if len(patients_list) > 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Mehrere Patienten mit der "
                                 f"Mobilfunknummer {cell_phone} gefunden")
                    return render(request, 'reports/patients.html', {'patients_list': patients_list})
                elif len(patients_list) == 1:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Patient mit der "
                                 f"Mobilfunknummer: {cell_phone} gefunden")
                    return redirect('/reports/patient/' + str(patients_list[0].id) + '/')
                else:
                    logger.debug(f"User-ID: {request.user.id}; search_patient: Kein Patient mit der "
                                 f"Mobilfunknummer: {cell_phone} gefunden")
                    return redirect('/reports/')

            else:
                logger.debug(f"User-ID: {request.user.id}; search_patient: Kein Suchkriterium eingegeben ")
                return redirect('/reports/')
    else:
        logger.debug(f"User-ID: {request.user.id}; search_patient: Kein POST Befehl erhalten")
        return redirect('/reports/')
    return render(request, 'reports/index_parents.html', {'form': form})


@permission_required('reports.add_patient')
def add_patient(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_patient: add patient with ID: "
                        f"'pa{str(item.id)}'; "
                        f"[ pa_first_name: {str(item.pa_first_name)},pa_last_name: {str(item.pa_last_name)},"
                        f"pa_street: {str(item.pa_street)},pa_zip_code: {str(item.pa_zip_code)},"
                        f"pa_city: {str(item.pa_city)},pa_phone: {str(item.pa_phone)},"
                        f"pa_cell_phone: {str(item.pa_cell_phone)},pa_cell_phone_add1: {str(item.pa_cell_phone_add1)},"
                        f"pa_cell_phone_add2: {str(item.pa_cell_phone_add2)},pa_cell_phone_sms: {str(item.pa_cell_phone_sms)},"
                        f"pa_email: {str(item.pa_email)},pa_date_of_birth: {str(item.pa_date_of_birth)},"
                        f"pa_gender: {str(item.pa_gender)},pa_active_no_yes: {str(item.pa_active_no_yes)},"
                        f"pa_invoice_mail: {str(item.pa_invoice_mail)},pa_sms_no_yes: {str(item.pa_sms_no_yes)},"
                        f"pa_email_no_yes: {str(item.pa_email_no_yes)} ]")
            return redirect('/reports/patient/' + str(item.id) + '/')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_patient: Formular aufgerufen")
        form = PatientForm()

    logger.info(f"User-ID: {request.user.id}; add_Patient: POST")
    return render(request, 'reports/patient_form.html', {'form': form})


@permission_required('reports.change_patient')
def edit_patient(request, id=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    item = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_patient: edit patient with ID: 'pa{str(item.id)}'; "
                    f"[ pa_first_name: {str(item.pa_first_name)},pa_last_name: {str(item.pa_last_name)},"
                    f"pa_street: {str(item.pa_street)},pa_zip_code: {str(item.pa_zip_code)},"
                    f"pa_city: {str(item.pa_city)},pa_phone: {str(item.pa_phone)},"
                    f"pa_cell_phone: {str(item.pa_cell_phone)},pa_cell_phone_add1: {str(item.pa_cell_phone_add1)},"
                    f"pa_cell_phone_add2: {str(item.pa_cell_phone_add2)},pa_cell_phone_sms: {str(item.pa_cell_phone_sms)},"
                    f"pa_email: {str(item.pa_email)},pa_date_of_birth: {str(item.pa_date_of_birth)},"
                    f"pa_gender: {str(item.pa_gender)},pa_active_no_yes: {str(item.pa_active_no_yes)},"
                    f"pa_invoice_mail: {str(item.pa_invoice_mail)},pa_sms_no_yes: {str(item.pa_sms_no_yes)},"
                    f"pa_email_no_yes: {str(item.pa_email_no_yes)} ]")

        return redirect('/reports/patient/' + str(item.id) + '/')
    logger.debug(f"User-ID: {request.user.id}; edit_patient: patient with ID: 'pa{str(id)}' called")
    form.id = item.id
    return render(request, 'reports/patient_form.html', {'form': form})


@permission_required('reports.view_patient')
def patient(request, id=id):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
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

        if Document.objects.filter(patient_id=patient_result.id, registration_form=1).exists():
            registration_form_exist = True
        else:
            registration_form_exist = False

        parents_form_exist = ''
        #ts = str(patient_result.pa_date_of_birth)
        #f = '%Y-%m-%d %H:%M:%S'
        f = '%Y-%m-%d'
        print(str(datetime.datetime.strptime(str(patient_result.pa_date_of_birth), f)))
        print(str(datetime.datetime.now()-datetime.timedelta(days=5475)))
        if datetime.datetime.strptime(str(patient_result.pa_date_of_birth), f) > datetime.datetime.now()-datetime.timedelta(days=5475):
            if Document.objects.filter(patient_id=patient_result.id, parents_form=1).exists():
                parents_form_exist = '1'
            else:
                parents_form_exist = '0'

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
                logger.debug(f"User-ID: {request.user.id}; patient: therapy_result_item Try Exception")
            i = i + 1
        logger.info(f"User-ID: {request.user.id}; patient: call patient with ID: 'pa{str(id)}' ")
        return render(request, 'reports/patient.html', {'patient': patient_result,
                                                        'therapy': therapy_result,
                                                        'ps': patient_something_value,
                                                        'therapy_count': therapy_result_count,
                                                        'process_count': process_result_count,
                                                        'registration_form_exist': registration_form_exist,
                                                        'parents_form_exist': parents_form_exist
                                                        })
    except ObjectDoesNotExist:
        logger.debug(f"User-ID: {request.user.id}; patient: Objekt existiert nicht")
        return redirect('/reports/')


##########################################################################
# Area Patient Sonstiges create and change
##########################################################################
@permission_required('reports.add_patient_something')
def add_pa_something(request):
    if request.method == "POST":
        form = PatientSomethingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_pa_something: 'pa_som{str(item.id)}'")
            return redirect('/reports/patient/' + str(request.POST.get('patient')))
    else:
        logger.debug(f"User-ID: {request.user.id}; add_pa_something: Formular zur Bearbeitung/Erfassung "
                     f"des Sonstiges-Feld am Patienten")
        patient_result = Patient.objects.get(id=request.GET.get('id'))
        form = PatientSomethingForm(initial={'patient': patient_result})
    return render(request, 'reports/pa_something_form.html', {'form': form})


@permission_required('reports.change_patient_something')
def edit_pa_something(request, id=None):
    item = get_object_or_404(Patient_Something, id=id)
    form = PatientSomethingForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_pa_something: 'pa_som{str(item.id)}'")
        return redirect('/reports/patient/' + str(item.patient_id))
    logger.debug(f"User-ID: {request.user.id}; edit_pa_something: Sonstige Form aufgerufen für ID: {id}")
    return render(request, 'reports/pa_something_form.html', {'form': form})


##########################################################################
# Area Initial Assessment create and change
##########################################################################
@permission_required('reports.add_initialassessment')
def add_ia(request):
    if request.method == "POST":
        form = InitialAssessmentForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_ia: 'ia{str(item.id)}'")
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=1')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_ia: Formular zur Bearbeitung/Erfassung des Erstbefunds")
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = InitialAssessmentForm(initial={'therapy': therapy_result})
    return render(request, 'reports/ia_form.html', {'form': form})


@permission_required('reports.change_initialassessment')
def edit_ia(request, id=None):
    item = get_object_or_404(InitialAssessment, id=id)
    form = InitialAssessmentForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_ia: 'ia{str(item.id)}'")
        return redirect('/reports/therapy/' + str(item.therapy_id) + '/?window=1')
    logger.debug(f"User-ID: {request.user.id}; edit_ia: Erstbefund Form angerufen mit ID: {id}")
    return render(request, 'reports/ia_form.html', {'form': form})


##########################################################################
# Area Therapy Sonstiges create and change
##########################################################################
@permission_required('reports.add_therapy_something')
def add_therapy_something(request):
    if request.method == "POST":
        form = TherapySomethingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_therapy_something: 'the_som{str(item.id)}'")
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=2')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_therapy_something: Formular zur Bearbeitung/Erfassung "
                     f"des Sonstiges-Feld")
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = TherapySomethingForm(initial={'therapy': therapy_result})
    return render(request, 'reports/something_form.html', {'form': form})


@permission_required('reports.change_therapy_something')
def edit_therapy_something(request, id=None):
    item = get_object_or_404(Therapy_Something, id=id)
    form = TherapySomethingForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_therapy_something: 'the_som{str(item.id)}'")
        return redirect('/reports/therapy/' + str(item.therapy_id) + '/?window=2')
    logger.debug(f"User-ID: {request.user.id}; edit_therapy_something: Sonstige Form aufgerufen für ID: {id}")
    return render(request, 'reports/something_form.html', {'form': form})


##########################################################################
# Area Therapy create and change
##########################################################################

@permission_required('reports.add_therapy')
def add_therapy(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    if request.method == "POST":
        form = TherapyForm(request.POST)
        patient_result = Patient.objects.get(id=request.POST.get('patients'))
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_therapy: for patient with ID: "
                        f"'pa{str(patient_result.id)}_th{item.id}'; "
                        f"[ recipe_date: {str(item.recipe_date)},"
                        f"therapy_regulation_amount: {str(item.therapy_regulation_amount)},"
                        f"therapy_duration: {str(item.therapy_duration)},"
                        f"therapy_frequence: {str(item.therapy_frequence)},"
                        f"therapy_rid_of: {str(item.therapy_rid_of)},"
                        f"therapy_report_no_yes: {str(item.therapy_report_no_yes)},"
                        f"therapy_homevisit_no_yes: {str(item.therapy_homevisit_no_yes)},"
                        f"therapy_indication_key: {str(item.therapy_icd_cod)},"
                        f"therapy_icd_cod: {str(item.therapy_icd_cod)},"
                        f"therapy_icd_cod_2: {str(item.therapy_icd_cod_2)},"
                        f"therapy_icd_cod_3: {str(item.therapy_icd_cod_3)},"
                        f"therapy_doctor: {str(item.therapy_doctor)},"
                        f"patients: {str(item.patients)},"
                        f"therapists: {str(item.therapists)},"
                        f"diagnostic_group: {str(item.diagnostic_group)},"
                        f"first_diagnostic_no_yes: {str(item.first_diagnostic_no_yes)},"
                        f"need_diagnostic_no_yes: {str(item.need_diagnostic_no_yes)},"
                        f"continue_diagnostic_no_yes: {str(item.continue_diagnostic_no_yes)} ]"
                        )

            return redirect('/reports/patient/' + str(patient_result.id) + '/')
        else:
            logger.info(f"User-ID: {request.user.id}; Dates not valid")
    else:
        logger.info(f"User-ID: {request.user.id}; add_therapy: Formular aufgerufen um eine Rezept anzulegen")
        form = TherapyForm(initial={'patients': request.GET.get('id')})
        patient_result = Patient.objects.get(id=request.GET.get('id'))
    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': patient_result})


@permission_required('reports.change_therapy')
def edit_therapy(request, id=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    item = get_object_or_404(Therapy, id=id)
    form = TherapyForm(request.POST or None, instance=item)

    if form.is_valid():
        patient_result = Patient.objects.get(id=request.POST.get('patients'))
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_therapy: edit therapy for patient "
                    f"with ID: 'pa{str(patient_result.id)}_th{item.id}'; "
                    f"[ recipe_date: {str(item.recipe_date)},therapy_regulation_amount): {str(item.therapy_regulation_amount)},"
                    f"therapy_duration: {str(item.therapy_duration)},therapy_frequence: {str(item.therapy_frequence)},"
                    f"therapy_rid_of: {str(item.therapy_rid_of)},"
                    f"therapy_report_no_yes: {str(item.therapy_report_no_yes)},"
                    f"therapy_homevisit_no_yes: {str(item.therapy_homevisit_no_yes)},"
                    f"therapy_indication_key: {str(item.therapy_icd_cod)},"
                    f"therapy_icd_cod: {str(item.therapy_icd_cod)},"
                    f"therapy_icd_cod_2: {str(item.therapy_icd_cod_2)},"
                    f"therapy_icd_cod_3: {str(item.therapy_icd_cod_3)},"
                    f"therapy_doctor: {str(item.therapy_doctor)},"
                    f"patients: {str(item.patients)},"
                    f"therapists: {str(item.therapists)},"
                    f"diagnostic_group: {str(item.diagnostic_group)},"
                    f"first_diagnostic_no_yes: {str(item.first_diagnostic_no_yes)},"
                    f"need_diagnostic_no_yes: {str(item.need_diagnostic_no_yes)},"
                    f"continue_diagnostic_no_yes: {str(item.continue_diagnostic_no_yes)} ]"
                    )
        return redirect('/reports/therapy/' + str(item.id) + '/')
    logger.debug(f"User-ID: {request.user.id}; edit_therapy: Rezeptformular des Patienten "
                 f"mit der ID: {str(item.id)} zwecks Änderung aufgerufen")
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


@permission_required('reports.view_therapy')
def therapy(request, id=id):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
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
    logger.info(f"User-ID: {request.user.id}; therapy: call therapy with ID: 'th{str(id)}'")
    return render(request, 'reports/therapy.html', {'therapy': therapy_result,
                                                    'patient': patient_value,
                                                    'ia': ia_value,
                                                    'ts': therapy_something_value,
                                                    'therapy_report': therapy_report_value,
                                                    'process_report': process_report_value})


##########################################################################
# Area Process Report (in German: Verlaufsprotokol)
##########################################################################
@permission_required('reports.add_process_report')
def add_process_report(request):
    if request.method == "POST":
        form = ProcessReportForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_process_report: Verlaufsprotokoll "
                        f"gespeichert mit ID: {str(request.POST.get('therapy'))}")

            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=3')
    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = ProcessReportForm(initial={'process_treatment':
                                              Process_report.objects.filter(
                                                  therapy_id=request.GET.get('id')).count() + 1,
                                          'therapy': therapy_result})
        logger.debug(f"User-ID: {request.user.id}; add_process_report: Verlaufsprotokoll "
                     f"anlegen mit ID: {request.GET.get('id')}")
        return render(request, 'reports/process_report_form.html', {'form': form})


@permission_required('reports.change_process_report')
def edit_process_report(request, id=None):
    item = get_object_or_404(Process_report, id=id)
    form = ProcessReportForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_process_report: Verlaufsprotokoll "
                    f"ändern mit ID: {str(item.id)}")
        return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=3')
    logger.info(f"User-ID: {request.user.id}; edit_process_report: Verlaufsprotokoll anlegen mit ID: {id}")
    return render(request, 'reports/process_report_form.html', {'form': form})


@permission_required('reports.delete_process_report')
def delete_process_report(request, id=None):
    item = get_object_or_404(Process_report, id=id)
    therapy_id = item.therapy_id
    if item:
        item.delete()
        return redirect('/reports/therapy/' + str(therapy_id) + '/?window=3')
    else:
        return redirect('/reports/')


@permission_required('reports.view_process_report')
def process_report(request, id=id):
    process_report_element = Process_report.objects.get(id=id)
    logger.debug(f"User-ID: {request.user.id}; process_report: Verlaufsprotokoll mit ID: {id} anzeigen")
    return render(request, 'reports/process_report.html', {'process_report': process_report_element})


@permission_required('reports.view_process_report')
def show_process_report(request):
    therapy_start_value = ''
    therapy_end_value = ''
    id = request.GET.get('id')
    logger.info(f"User-ID: {request.user.id}; show_process_report2: Verlaufsreport mit ID: {id} gedruckt")
    therapy_value = Therapy.objects.get(id=id)
    therapy_value.pa_first_name = Therapy.objects.get(id=id).patients.pa_first_name
    therapy_value.pa_last_name = Therapy.objects.get(id=id).patients.pa_last_name
    therapy_value.print_date = datetime.datetime.now()
    if Therapy_report.objects.filter(therapy=id):
        therapy_report_value = Therapy_report.objects.get(therapy=id)
        therapy_value.therapy_start_value = therapy_report_value.therapy_start
        therapy_value.therapy_end_value = therapy_report_value.therapy_end

    process_report_value = Process_report.objects.filter(therapy=id)

    process_report_value.static_root = settings.STATIC_ROOT

    filename = "Verlauf_" + therapy_value.pa_last_name + "_" + therapy_value.pa_first_name + "_" + str(
        therapy_value.recipe_date) + ".pdf"

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
@permission_required('reports.add_therapy_report')
def add_therapy_report(request):
    if request.method == "POST":

        item = get_object_or_404(Therapy_report, therapy=request.POST.get('therapy'))
        form = TherapyReportForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            logger.info(f"User-ID: {request.user.id}; add_therapy_report: ID: "
                        f"'th{str(request.POST.get('therapy'))}_trr{str(item.id)}';"
                        f"[ report_date: {str(item.report_date)},"
                        f"therapy_start: {str(item.therapy_start)},"
                        f"therapy_end: {str(item.therapy_end)},"
                        f"therapy_indicated: {str(item.therapy_indicated)},"
                        f"therapy_break: {str(item.therapy_break)},"
                        f"therapy_break_internal: {str(item.therapy_break_internal)},"
                        f"therapy_break_date: {str(item.therapy_break_date)},"
                        f"therapy_comment: {str(item.therapy_comment)},"
                        f"therapy_individual: {str(item.therapy_individual)},"
                        f"therapy_individual_min: {str(item.therapy_individual_min)},"
                        f"therapy_group: {str(item.therapy_group)},"
                        f"therapy_group_min: {str(item.therapy_group_min)},"
                        f"therapy_finish: {str(item.therapy_finish)},"
                        f"therapy_re_introduction: {str(item.therapy_re_introduction)},"
                        f"therapy_re_introduction_weeks: {str(item.therapy_re_introduction_weeks)},"
                        f"therapy_frequence: {str(item.therapy_frequence)},"
                        f"therapy_frequence_count_per_week: {str(item.therapy_frequence_count_per_week)},"
                        f"therapy_another: {str(item.therapy_another)},"
                        f"therapy_another_text: {str(item.therapy_another_text)},"
                        f"therapy_home_visit: {str(item.therapy_home_visit)},"
                        f"therapy_necessary: {str(item.therapy_necessary)},"
                        f"therapy_report_variation: {str(item.therapy_report_variation)} ]")

            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/?window=4')
        else:
            return render(request, 'reports/therapy_report_form.html', {'form': form})

    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        Therapy_report.objects.create(report_date=datetime.date.today(), therapy=therapy_result)

        form = TherapyReportForm(initial={'therapy': therapy_result})
        logger.info(f"User-ID: {request.user.id}; add_therapy_report: Therapiebericht "
                    f"gespeichert mit ID: {str(request.POST.get('therapy'))}")
        return render(request, 'reports/therapy_report_form.html', {'form': form})


@permission_required('reports.change_therapy_report')
def edit_therapy_report(request, id=None):
    item = get_object_or_404(Therapy_report, id=id)
    form = TherapyReportForm(request.POST or None, instance=item)
    #print(request.POST)
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_therapy_report: ID: "
                    f"'th{str(request.POST.get('therapy'))}_trr{str(item.id)}';"
                    f"[ report_date: {str(item.report_date)},"
                    f"therapy_start: {str(item.therapy_start)},"
                    f"therapy_end: {str(item.therapy_end)},"
                    f"therapy_indicated: {str(item.therapy_indicated)},"
                    f"therapy_break: {str(item.therapy_break)},"
                    f"therapy_break_internal: {str(item.therapy_break_internal)},"
                    f"therapy_break_date: {str(item.therapy_break_date)},"
                    f"therapy_comment: {str(item.therapy_comment)},"
                    f"therapy_individual: {str(item.therapy_individual)},"
                    f"therapy_individual_min: {str(item.therapy_individual_min)},"
                    f"therapy_group: {str(item.therapy_group)},"
                    f"therapy_group_min: {str(item.therapy_group_min)},"
                    f"therapy_finish: {str(item.therapy_finish)},"
                    f"therapy_re_introduction: {str(item.therapy_re_introduction)},"
                    f"therapy_re_introduction_weeks: {str(item.therapy_re_introduction_weeks)},"
                    f"therapy_frequence: {str(item.therapy_frequence)},"
                    f"therapy_frequence_count_per_week: {str(item.therapy_frequence_count_per_week)},"
                    f"therapy_another: {str(item.therapy_another)},"
                    f"therapy_another_text: {str(item.therapy_another_text)},"
                    f"therapy_home_visit: {str(item.therapy_home_visit)},"
                    f"therapy_necessary: {str(item.therapy_necessary)},"
                    f"therapy_report_variation: {str(item.therapy_report_variation)} ]")

        return redirect('/reports/therapy/' + str(item.therapy_id) + '/?window=4')

    logger.debug(f"User-ID: {request.user.id}; edit_therapy_report: Therapiebericht anlegen mit ID: {id}")

    return render(request, 'reports/therapy_report_form.html', {'form': form})


@permission_required('reports.change_therapy_report')
def save_therapyreport_element(request):
    # logger.info("Hallo Start")
    if request.is_ajax():
        id_therapy = request.POST.get('id_therapy')
        data_field = request.POST.get('field')
        item = get_object_or_404(Therapy_report, therapy=id_therapy)
        content = request.POST.get('content')

        if data_field == 'therapy_therapist_diagnostic':
            setattr(item, 'therapy_therapist_diagnostic', content)
        elif data_field == 'therapy_status':
            setattr(item, 'therapy_status', content)
        elif data_field == 'therapy_aims':
            setattr(item, 'therapy_aims', content)
        elif data_field == 'therapy_content':
            setattr(item, 'therapy_content', content)
        elif data_field == 'therapy_process':
            setattr(item, 'therapy_process', content)
        elif data_field == 'therapy_compliance':
            setattr(item, 'therapy_compliance', content)
        elif data_field == 'therapy_summary':
            setattr(item, 'therapy_summary', content)
        elif data_field == 'therapy_forecast':
            setattr(item, 'therapy_forecast', content)
        elif data_field == 'therapy_emphases':
            setattr(item, 'therapy_emphases', content)
        elif data_field == 'therapy_current_result':
            setattr(item, 'therapy_current_result', content)

        item.save()
        # print("ID: " + id + "; data_field: " + data_field + "; " + content)

        return JsonResponse({
            'msg': 'Success'
        })

    return JsonResponse({
        'msg': 'Error'
    })


@permission_required('reports.view_therapy_report')
def therapy_report(request, id=id):
    therapy_report = Therapy_report.objects.get(id=id)
    logger.info(f"User-ID: {request.user.id}; therapy_report: call report with ID: 'trr{id}'")
    return render(request, 'reports/therapy_report_standard.html', {'therapy_report': therapy_report})


@permission_required('reports.delete_therapy_report')
def show_therapy_report(request):
    id = request.GET.get('id')
    logger.info(f"User-ID: {request.user.id}; show_therapy_report: show therapy report with  ID: 'trr{id}' gedruckt")
    therapy_result = Therapy.objects.get(id=request.GET.get('id'))
    result = Therapy_report.objects.get(therapy=request.GET.get('id'))
    doctor_result = Doctor.objects.get(id=therapy_result.therapy_doctor_id)
    result.pa_first_name = therapy_result.patients.pa_first_name
    result.pa_last_name = therapy_result.patients.pa_last_name
    result.pa_date_of_birth = therapy_result.patients.pa_date_of_birth
    result.recipe_date = therapy_result.recipe_date
    result.therapy_regulation_amount = therapy_result.therapy_regulation_amount
    result.process_count = Process_report.objects.filter(therapy=id).count()
    result.static_root = settings.STATIC_ROOT

    report_variation = result.therapy_report_variation

    if report_variation == 0:
        html_file = 'pdf_templates/therapy_report_short.html'
        css_file = '/reports/therapy_report_short.css'
    elif report_variation == 1:
        html_file = 'pdf_templates/therapy_report_standard.html'
        css_file = '/reports/therapy_report_standard.css'
    else:
        html_file = 'pdf_templates/therapy_report_big.html'
        css_file = '/reports/therapy_report_big.css'

    filename = result.pa_last_name + "_" + result.pa_first_name + "_" + str(result.recipe_date) + ".pdf"

    html_string = render_to_string(html_file, {'therapy': therapy_result, 'result': result, 'doctor': doctor_result})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    logger.debug(f"User-ID: {request.user.id}; show_therapy_report CSS_File: {settings.STATIC_ROOT}{css_file}")
    pdf = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + css_file)])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    return response


@permission_required('reports.add_wait_list')
def add_waitlist(request):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    if request.method == "POST":
        form = WaitlistForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            logger.info(f"User-ID: {request.user.id}; add_waitlist: Waitlist "
                        f"mit der ID: 'wl{str(item.id)}' gespeichert")
            return redirect('/reports/edit/waitlist/' + str(item.id) + '/')
        else:
            print('Problems with form')
    else:
        logger.debug(f"User-ID: {request.user.id}; add_waitlist: Formular aufgerufen")
        form = WaitlistForm()
    return render(request, 'reports/waitlist_form.html', {'form': form})


@permission_required('reports.change_wait_list')
def edit_waitlist(request, id=None):
    double_entry = 0
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    item = get_object_or_404(Wait_list, id=id)
    form = WaitlistForm(request.POST or None, instance=item)
    patient = Patient.objects.filter(pa_last_name=item.wl_last_name, pa_first_name=item.wl_first_name)
    if patient:
        double_entry = 1
    if form.is_valid():
        form.save()
        logger.info(f"User-ID: {request.user.id}; edit_waitlist: Wait_list mit der ID: 'wl{str(item.id)}' geändert")
        return redirect('/reports/edit/waitlist/' + str(item.id) + '/')
    logger.debug(f"User-ID: {request.user.id}; edit_waitlist: Wait-list "
                 f"mit der ID: {str(id)} zwecks Änderung aufgerufen")
    form.id = item.id
    form.double_entry = double_entry
    return render(request, 'reports/waitlist_form.html', {'form': form})


@permission_required('reports.view_wait_list')
def waitlist(request, status):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    waitlist = Wait_list.objects.filter(wl_active=status).order_by('wl_call_date')

    for waitlist_item in waitlist:
        waitlist_item.wl_phone = get_phone_design(waitlist_item.wl_phone)
        waitlist_item.wl_cell_phone = get_phone_design(waitlist_item.wl_cell_phone)
        patient = Patient.objects.filter(pa_last_name=waitlist_item.wl_last_name,
                                         pa_first_name=waitlist_item.wl_first_name)
        if patient:
            waitlist_item.double_entry = 1

    logger.info(f"User-ID: {request.user.id}; waitlist: Wait_list aufgerufen")
    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': status})


@permission_required('reports.view_wait_list')
def copy_waitlist_item(request, id=id):
    waitlist = get_object_or_404(Wait_list, id=id)
    patient = Patient.objects.filter(pa_last_name=waitlist.wl_last_name, pa_first_name=waitlist.wl_first_name)

    if patient:
        waitlist.double_entry = 1
        for item in patient:
            waitlist.pa_date_of_birth = item.pa_date_of_birth

    if request.GET['status'] == 'no':
        return render(request, 'reports/waitlist_confirm_create.html', {'waitlist': waitlist})
    else:
        # create patient_object
        try:
            if waitlist.wl_date_of_birth == None:
                waitlist.wl_date_of_birth = "1900-01-01"

            Patient.objects.create(pa_first_name=waitlist.wl_first_name,
                                   pa_last_name=waitlist.wl_last_name,
                                   pa_street=waitlist.wl_street,
                                   pa_city=waitlist.wl_city,
                                   pa_zip_code=waitlist.wl_zip_code,
                                   pa_date_of_birth=waitlist.wl_date_of_birth,
                                   pa_phone=waitlist.wl_phone,
                                   pa_cell_phone=waitlist.wl_cell_phone,
                                   pa_cell_phone_add1=waitlist.wl_cell_phone_add1,
                                   pa_cell_phone_add2=waitlist.wl_cell_phone_add2,
                                   pa_cell_phone_sms=waitlist.wl_cell_phone_sms,
                                   pa_email=waitlist.wl_email,
                                   pa_gender=waitlist.wl_gender,
                                   pa_note=waitlist.wl_information
                                   )
            # set status waitlist object to False
            waitlist.wl_active = False
            waitlist.save()
            logger.info(f"User-ID: {request.user.id}; copy_waitlist_item: Patient wurde "
                        f"erfolgreich aus Warteliste angelegt")

        except Exception as e:
            logger.info(f"User-ID: {request.user.id}; copy_waitlist_item: Fehler beim speichern: {str(e)}")

    # Info to Webfrontwend
    waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')
    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})


class delete_waitlist_item(DeleteView):
    model = Wait_list
    template_name = 'reports/waitlist_confirm_delete.html'
    context_object_name = 'waitlist'
    success_url = reverse_lazy('reports:waitlist', kwargs=dict(status='False'))


@permission_required('reports.change_wait_list')
def set_waitlist_item_inactive(request, id=None):
    item = get_object_or_404(Wait_list, id=id)
    if item:
        item.wl_active = False
        item.save()
        logger.info(f"User-ID: {request.user.id}; set_waitlist_item_inactive: set item 'wl{str(item.id)}' inactive")
    else:
        logger.info(f"User-ID: {request.user.id}; set_waitlist_item_inactive: can't set 'wl{str(item.id)}' inactive")
    waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')

    for waitlist_item in waitlist:
        waitlist_item.wl_phone = get_phone_design(waitlist_item.wl_phone)
        waitlist_item.wl_cell_phone = get_phone_design(waitlist_item.wl_cell_phone)
        patient = Patient.objects.filter(pa_last_name=waitlist_item.wl_last_name,
                                         pa_first_name=waitlist_item.wl_first_name)
        if patient:
            waitlist_item.double_entry = 1

    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})


@permission_required('reports.change_wait_list')
def set_waitlist_item_active(request, id=None):
    item = get_object_or_404(Wait_list, id=id)
    if item:
        item.wl_active = True
        item.save()
        logger.info(f"User-ID: {request.user.id}; set_waitlist_item_active: set item 'wl{str(item.id)}' active")

    else:
        logger.info(f"User-ID: {request.user.id}; set_waitlist_item_active: can't set 'wl{str(item.id)}' active")

    waitlist = Wait_list.objects.filter(wl_active=True).order_by('wl_call_date')

    for waitlist_item in waitlist:
        waitlist_item.wl_phone = get_phone_design(waitlist_item.wl_phone)
        waitlist_item.wl_cell_phone = get_phone_design(waitlist_item.wl_cell_phone)
        patient = Patient.objects.filter(pa_last_name=waitlist_item.wl_last_name,
                                         pa_first_name=waitlist_item.wl_first_name)
        if patient:
            waitlist_item.double_entry = 1

    return render(request, 'reports/waitlist.html', {'waitlist': waitlist, 'status': 'True'})


##########################################################################
# Area Document upload
##########################################################################

@permission_required('reports.view_patient')
def upload_document(request):
    if request.method == 'POST':
        item_form = DocumentForm(request.POST, request.FILES)
        patient_result = Patient.objects.get(id=request.POST.get('patient'))
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.patient_id = patient_result.id
            item.save()
            logger.debug(f"User-ID: {request.user.id}; upload_document: document {str(item.id)} uploaded")
            return redirect('/reports/document/?id=' + str(patient_result.id))
    else:
        logger.debug(f"User-ID: {request.user.id}; upload_document: Formular aufgerufen um Dokumente "
                     f"zu sehen oder hochzuladen")
        form = DocumentForm(initial={'patient': request.GET.get('id')})
        patient_result = Patient.objects.get(id=request.GET.get('id'))
        documents_registration = Document.objects.filter(patient_id=request.GET.get('id'), registration_form=1)
        documents_parents = Document.objects.filter(patient_id=request.GET.get('id'), parents_form=1)
        documents = Document.objects.filter(patient_id=request.GET.get('id'),
                                            registration_form=0, parents_form=0).order_by('-uploaded_at')
    return render(request, 'reports/document_form.html',
                  {'form': form, 'patient': patient_result, 'documents': documents,
                   'documents_registration': documents_registration,
                   'documents_parents': documents_parents})


IMAGE_FILE_TYPES = ['pdf']


@permission_required('reports.view_patient')
def download_document(request):
    if request.method == 'GET':
        file_id = request.GET.get('id')
        logger.info(f"User-ID: {request.user.id}; download_document: document {file_id} downloaded")
        file_info = Document.objects.get(id=file_id)
        document_name = file_info.document.name
        document_path = settings.MEDIA_ROOT + '/' + document_name
        response = FileResponse(open(document_path, 'rb'), as_attachment=True)
        return response

    logger.debug(f"User-ID: {request.user.id}; download_document: keine Get-Methode beim Download")
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
            logger.info(f"User-ID: {request.user.id}; del_document: document: {document_name} deleted")
        else:
            logger.info(f"User-ID: {request.user.id}; del_document: document: {document_path} can't be deleted ")

        return HttpResponseRedirect(self.success_url + "?id=" + patient_id)


##########################################################################
# Area Document upload
##########################################################################

@permission_required('reports.view_patient')
def upload_document_therapy(request):
    if request.method == 'POST':
        item_form = DocumentTherapyForm(request.POST, request.FILES)
        therapy_result = Therapy.objects.get(id=request.POST.get('therapy'))
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.therapy_id = therapy_result.id
            item.save()
            logger.info(f"User-ID: {request.user.id}; upload_document_therapy: document {item.id} uploaded")
            return redirect('/reports/document_therapy/?id=' + str(therapy_result.id))
    else:
        logger.debug(f"User-ID: {request.user.id}; upload_document_therapy: Formular aufgerufen um Dokumente "
                     f"zu sehen oder hochzuladen")
        form = DocumentTherapyForm(initial={'therapy': request.GET.get('id')})
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        documents = Document_therapy.objects.filter(therapy_id=request.GET.get('id')).order_by('-uploaded_at')
    return render(request, 'reports/document_therapy_form.html',
                  {'form': form, 'therapy': therapy_result, 'documents': documents})


IMAGE_FILE_TYPES = ['pdf']


@permission_required('reports.view_patient')
def download_document_therapy(request):
    if request.method == 'GET':
        file_id = request.GET.get('id')
        file_info = Document_therapy.objects.get(id=file_id)
        document_name = file_info.document.name
        document_path = settings.MEDIA_ROOT + '/' + document_name
        logger.info(f"User-ID: {request.user.id}; download_document_therapy: document: {document_name} downloaded")
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
            logger.info(f"User-ID: {request.user.id}; del_document_therapy: document: {document_name} deleted")
        else:
            logger.info(f"User-ID: {request.user.id}; del_document_therapy: document: {document_path} can't be deleted")

        return HttpResponseRedirect(self.success_url + "?id=" + therapy_id)


@permission_required('reports.view_patient')
def get_session_timer(request):
    if request.is_ajax and request.method == "GET":
        sessiontimer = request.session.get_expiry_date().isoformat()
        logger.debug(f"User-ID: {request.user.id}; get_session_timer: {str(sessiontimer)}")
        return JsonResponse({'sessiontimer': sessiontimer}, status=200)

    return JsonResponse({"error": ""}, status=400)


# Die Klasse ist für getOpenReports wichtig!!!
class openContext:
    pass


@permission_required('reports.view_patient')
def getOpenReports(request, context=None):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
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
                logger.debug(f"User-ID: {request.user.id}; Try Exception")

            if not report_date_value:
                patient_value = Patient.objects.filter(id=tp_item.patients.id)
                tp_item.pa_last_name = patient_value[0].pa_last_name
                tp_item.pa_first_name = patient_value[0].pa_first_name
                reports_list.append(tp_item)

    # Ermittlung der Therapieberichte bei den "Pause" ausgewählt ist
    if request.user.groups.filter(name='Leitung').exists():
        therapybreak_count = Therapy_report.objects. \
            select_related('therapy__patients'). \
            filter(therapy_break_internal=True,
                   therapy_end__lte=datetime.date.today() + datetime.timedelta(days=-21),
                   therapy__patients__pa_active_no_yes=True).count()
    else:
        therapybreak_count = Therapy_report.objects. \
            select_related('therapy__patients'). \
            filter(therapy_break_internal=True,
                   therapy_end__lte=datetime.date.today() + datetime.timedelta(days=-21),
                   therapy__therapists__tp_user_logopakt=str(request.user),
                   therapy__patients__pa_active_no_yes=True).count()

    openReports = len(reports_list)

    # context = {'getOpenReports': str(openReports)}
    openContext.getOpenReports = str(openReports)
    openContext.therapybreak_count = str(therapybreak_count)
    logger.debug(f"User-ID: {request.user.id}; getOpenReports aufgerufen")

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
        if "(" in data[1]:
            rightdata = data[1].rsplit("(")
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
        else:
            data[1] = data[1].replace(' ', '')
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

        data[0] = data[0].replace(' ', '')

        if "(" in data[1]:
            data = data[0] + " / " + charvalue + "  (" + rightdata[1]
        else:
            data = data[0] + " / " + charvalue
        return data


# helper function
def send_personal_mail(user, request):
    logger.debug(f"User-ID: {user.id}; Sending an email")
    logger.info(f"User-ID: {user.id}; {format(user)} E-Mail senden wegen neuem Gerät")
    subject = 'Anmeldung an der Anwendung LogoPAkt'
    from_email = 'logopakt@logoeu.uber.space'
    email_list = [user.email]

    openContext.static_root = settings.STATIC_ROOT
    openContext.media_root = settings.MEDIA_ROOT
    openContext.user = user
    image = 'logopaedie.png'
    file_path = os.path.join(settings.STATIC_ROOT + '/images/', image)
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)

    text_content = 'Sie haben sich gerade an der Anwendung LogoPAkt angemeldet. Sollte dies nicht stimmen, ' \
                   'bitte umgehend Toni Schumacher informieren!!!'
    html_content = render_to_string('mail_templates/login_mail.html',
                                    {'openContext': openContext, 'meta': request.META})

    msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
    msg.mixed_subtype = 'related'
    msg.attach_alternative(html_content, "text/html")
    msg.attach(img)
    msg.send()
    logger.debug(f"User-ID: {user.id}; EMail was send")


@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    logger.debug(f"User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                 f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}")
    logger.info(f"User-ID: {request.user.id}; {format(user)} log in")
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    elif request.META.get('REMOTE_ADDR'):
        ip_address = request.META.get('REMOTE_ADDR')
    else:
        ip_address = "nothing"

    logger.debug(f"User-ID: {request.user.id}; SESSION_EXPIRE_SECONDS: {settings.SESSION_EXPIRE_SECONDS}")

    http_user_agent = request.META.get('HTTP_USER_AGENT')
    logger.debug(f"User-ID: {request.user.id}; User Agent: {http_user_agent}")

    try:
        Login_Failed.objects.filter(user_name=user).delete()
        logger.debug(f"User-ID: {request.user.id}; Userdaten von {format(user)} in failed_login gelöscht")
    except:
        logger.debug(f"User-ID: {request.user.id}; User not found")

    try:
        login_user_agent = Login_User_Agent.objects.get(ip_address=ip_address, user_agent=http_user_agent)
        login_user_agent.last_login = datetime.datetime.now(tz=timezone.utc)
        login_user_agent.save()
        logger.debug(f"User-ID: {request.user.id}; post_login; check user_agent; result: Do nothing")
    except:
        login_user_agent = Login_User_Agent(user_name=request.user, ip_address=ip_address, user_agent=http_user_agent)
        login_user_agent.save()
        logger.debug(f"User-ID: {request.user.id}; post_login; check user_agent; result: send e-mail to {user}")
        send_personal_mail(user, request)


@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    logger.info(f"Post_logout: User-ID: {request.user.id}; Sessions-ID: {request.session.session_key}; "
                f"{request.session.get_expiry_date()}; {datetime.datetime.utcnow()}; Logout")

    try:
        logger.info(f"User-ID: {request.user.id}; ausgeloggt")
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
            logger.debug(f"User-ID: {request.user.id}; Fehlversuche: {credentials['username']} : {str(x)}")
            user_local.request_status = 'A'
            user_local.is_active = False
            user_local.save()
            send_mail(
                subject='ACHTUNG: Anmeldefehlversuche logoPAkt!!!',
                message='User: ' + credentials['username'] + ' hat sich mehr als ' + str(
                    x) + 'x mit falschem Passwort eingeloggt und wurde deaktiviert',
                from_email='logopakt@logoeu.uber.space',
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
            logger.info(f"User-ID: {request.user.id};  Fehlversuche: {request.META['REMOTE_ADDR']} : {str(x)}")
            send_mail(
                subject='ACHTUNG: Anmeldefehlversuche logoPAkt!!!',
                message='IP-Adresse: ' + request.META['REMOTE_ADDR'] + ' hat sich mehr als ' + str(
                    x) + 'x mit falschem Benutzernamen eingeloggt',
                from_email='logopakt@logoeu.uber.space',
                recipient_list=['norbert.krings@gmail.com', ],
                fail_silently=False,
            )


class meta_info:
    pass


def list_meta_info(request):
    meta_info.CONTENT_LENGTH = request.META.get('CONTENT_LENGTH')
    meta_info.CONTENT_TYPE = request.META.get('CONTENT_TYPE')
    meta_info.HTTP_ACCEPT = request.META.get('HTTP_ACCEPT')
    meta_info.HTTP_ACCEPT_ENCODING = request.META.get('HTTP_ACCEPT_ENCODING')
    meta_info.HTTP_ACCEPT_LANGUAGE = request.META.get('HTTP_ACCEPT_LANGUAGE')
    meta_info.HTTP_HOST = request.META.get('HTTP_HOST')
    meta_info.HTTP_REFERER = request.META.get('HTTP_REFERER')
    meta_info.HTTP_USER_AGENT = request.META.get('HTTP_USER_AGENT')
    meta_info.QUERY_STRING = request.META.get('QUERY_STRING')
    meta_info.REMOTE_ADDR = request.META.get('REMOTE_ADDR')
    meta_info.REMOTE_HOST = request.META.get('REMOTE_HOST')
    meta_info.REMOTE_USER = request.META.get('REMOTE_USER')
    meta_info.REQUEST_METHOD = request.META.get('REQUEST_METHOD')
    meta_info.SERVER_NAME = request.META.get('SERVER_NAME')
    meta_info.SERVER_PORT = request.META.get('SERVER_PORT')

    return render(request, 'reports/list_meta_info.html', {'meta_info': meta_info, 'meta': request.META})


def readShortcuts(request):
    if request.is_ajax and request.method == "GET":
        shortcuts = Shortcuts.objects.all()

        data = serialize("json", shortcuts, fields=('short', 'long'))
        logger.debug(f"User-ID: {request.user.id}; Shortcuts gelesen")
        return JsonResponse({'shortcuts': data}, status=200)

    logger.debug(f"User-ID: {request.user.id}; Shortcuts konnten nicht gelesen werden")
    return JsonResponse({"error": ""}, status=400)
# **************************************************************************************************
