import logging
import os
import uuid
import qrcode
import base64
#import pdb

from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer
from formtools.wizard.views import SessionWizardView

from weasyprint import HTML, CSS

from parents.forms import (ParentsSheetFormStep1, ParentsSheetFormStep2, ParentsSheetFormStep3,
                           ParentsSheetFormStep4, ParentsSheetFormStep5, ParentsSheetFormStep6, ParentsSheetForm,
                           ParentsSheetListForm)

from parents.models import Parents_sheet

from reports.models import Patient, Document

logger = logging.getLogger(__name__)

# assert False

class ParentsSheetWizard(SessionWizardView):
    form_list = [
        ParentsSheetFormStep1,
        ParentsSheetFormStep2,
        ParentsSheetFormStep3,
        ParentsSheetFormStep4,
        ParentsSheetFormStep5,
        ParentsSheetFormStep6
    ]

    template_name = 'parents/parents_form.html'

    def get_form_kwargs(self, step=None):
        # Hol dir Standard-kwargs
        kwargs = super().get_form_kwargs(step)

        # Übergib den User an die Form
        kwargs.update({'user': self.request.user})
        return kwargs

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        parents_sheet = Parents_sheet.objects.create(**data)
        return redirect('/parents/success/')


class ParentsSheetListView(ListView):
    model = Parents_sheet
    template_name = "parents/parents_sheet_liste.html"
    context_object_name = "parents_sheet_list"

    def get_queryset(self):
        queryset = Parents_sheet.objects.filter(sheet_created=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParentsSheetListForm()  # Leere Form für jeden Eintrag
        return context


class ParentsSheetUpdateView(UpdateView):
    model = Parents_sheet
    form_class = ParentsSheetForm
    template_name = "parents/parents_sheet_detail_form.html"
    context_object_name = "parents_sheet"
    success_url = reverse_lazy("parents:parents_sheet_list")


def generate_temporary_link():
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    patient_uuid = str(uuid.uuid4())
    token = s.dumps({"patient_uuid": patient_uuid})

    return f"{settings.URL_PARENTS}{token}/"


@login_required
def generate_qr_code(request):
    temp_link = generate_temporary_link()  # Temporären Link erstellen
    qr = qrcode.make(temp_link)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    #return HttpResponse(buffer.getvalue(), content_type="image/png")
    return render(request, 'parents/parents_qr_code.html', {"qr_code": qr_base64, "temp_link": temp_link})


@permission_required('reports.add_patient')
def move_parents_sheet_to_document(request, pk):
    parents_sheet = get_object_or_404(Parents_sheet, pk=pk)
    patientId = request.POST.get('patientId')

    filepath_doc = parents_sheet_report(str(pk), str(patientId))
    #print(f"PatientID: {patientId}")
    try:
        patient = Patient.objects.get(id=patientId)
        document = Document(description='Elternbogen', document=filepath_doc, patient=patient, parents_form=True)
        document.save()
    except Exception as e:
        logger.error(f"Fehler beim Datenbank-Update: {str(e)}")

    try:
        parents_sheet.sheet_created = True
        #parents_sheet.save(update_fields=["sheet_created"])
    except Exception as e:
        logger.error(f"Fehler beim Datenbank-Update: {str(e)}")

    return redirect('/reports/patient/' + str(patientId) + '/')


def parents_sheet_report(sourceId, targetId):

    parents_sheet = Parents_sheet.objects.get(id=sourceId)

    html_file = 'pdf_templates/parents_sheet_report.html'
    css_file = os.path.join(settings.STATIC_ROOT, 'parents/parents_sheet_report.css')
    html_string = render_to_string(html_file, {'parents_sheet': parents_sheet})

    filename = "Elternbogen_" + parents_sheet.child_last_name + "_" + parents_sheet.child_first_name + ".pdf"

    pdf_directory = os.path.join(settings.MEDIA_ROOT, "patient/" + targetId)
    os.makedirs(pdf_directory, exist_ok=True)  # Sicherstellen, dass der Ordner existiert

    pdf_path = os.path.join(pdf_directory, filename)
    filepath_doc = "patient/" + str(targetId) + "/" + filename

    HTML(string=html_string).write_pdf(pdf_path, stylesheets=[CSS(filename=css_file)])

    return filepath_doc

