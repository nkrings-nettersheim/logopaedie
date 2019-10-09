import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Patient, Therapy, Therapy_report, Process_report
from .forms import PatientForm, TherapyForm, TherapyReportForm
from .forms import SearchPatient


def index(request):
    template = loader.get_template('reports/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


class PatientView(generic.ListView):
    model = Patient
    template_name = 'reports/patients.html'
    context_object_name = 'patients_list'

    def get_queryset(self):
        return Patient.objects.all()


def search_patient(request):
    if request.method == 'POST':
        id = request.POST['patient_id']
        return redirect('/reports/patient/' + str(id) + '/')


def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_item = form.save(commit=False)
            patient_item.save()
            return redirect('/reports/patient/' + str(patient_item.id) + '/')
    else:
        form = PatientForm()
    return render(request, 'reports/patient_form.html', {'form': form})


def edit_patient(request, id=None):
    item = get_object_or_404(Patient, patient_id=id)
    form = PatientForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/reports/patient/' + str(item.patient_id) + '/')
    return render(request, 'reports/patient_form.html', {'form': form})


def patient(request, id=id):
    try:
        patient_result = Patient.objects.get(patient_id=id)
        patient_helper = patient_result.id
        therapy_result = Therapy.objects.filter(patients_id=patient_helper).order_by('-recipe_date')
        return render(request, 'reports/patient.html', {'patient': patient_result, 'therapy': therapy_result})
    except ObjectDoesNotExist:
        return redirect('/reports/')


def add_therapy(request):
    if request.method == "POST":
        form = TherapyForm(request.POST)
        patient_result = Patient.objects.get(id=request.POST.get('patients'))
        if form.is_valid():
                therapy_item = form.save(commit=False)
                therapy_item.save()
                return redirect('/reports/patient/' + str(patient_result.patient_id) + '/')
    else:
        form = TherapyForm(initial={'patients': request.GET.get('id')})
        patient_result = Patient.objects.get(id=request.GET.get('id'))
    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': patient_result})


def edit_therapy(request, id=None):
    item = get_object_or_404(Therapy, id=id)
    form = TherapyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/reports/therapy/' + str(item.id) + '/')

    return render(request, 'reports/therapy_form.html', {'form': form, 'patient': item.patients})


def therapy(request, id=id):
    therapy_result = Therapy.objects.get(id=id)
    patient_value = Patient.objects.get(id=str((therapy_result.patients.id)))
    therapy_report_value = Therapy_report.objects.filter(therapy_id=therapy_result.id)
    process_report_value = Process_report.objects.filter(patients_id=therapy_result.patients.id)
    return render(request, 'reports/therapy.html', {'therapy': therapy_result,
                                                    'patient': patient_value,
                                                    'therapy_report': therapy_report_value,
                                                    'process_report': process_report_value})


def add_therapy_report(request):
    if request.method == "POST":
        form = TherapyReportForm(request.POST)
        if form.is_valid():
            therapy_report_item = form.save(commit=False)
            therapy_report_item.save()
            return redirect('/reports/therapy/' + str(request.POST.get('therapy')) + '/')
    else:
        therapy_result = Therapy.objects.get(id=request.GET.get('id'))
        form = TherapyReportForm(initial={'therapy_treatment': Therapy_report.objects.filter(therapy_id=request.GET.get('id')).count() + 1, 'therapy': therapy_result})
        return render(request, 'reports/therapy_report_form.html', {'form': form})


def edit_therapy_report(request, id=None):
    item = get_object_or_404(Therapy_report, id=id)
    form = TherapyReportForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/reports/therapy_report/' + str(item.id) + '/')
    return render(request, 'reports/therapy_report_form.html', {'form': form})


def therapy_report(request, id=id):
    therapy_report = Therapy_report.objects.get(id=id)
    return render(request, 'reports/therapy_report.html', {'therapy_report': therapy_report})

#**************************************************************************************************

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
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
        }
    }
})

