import logging
import uuid
import qrcode
import base64
#import pdb

from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
#from itsdangerous.serializer import Serializer
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer

from parents.forms import (ParentsSheetFormStep1, ParentsSheetFormStep2, ParentsSheetFormStep3,
                           ParentsSheetFormStep4, ParentsSheetFormStep5, ParentsSheetFormStep6)

from parents.models import Parents_sheet

logger = logging.getLogger(__name__)

# assert False

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
    logger.info('Indexseite wurde geladen')

    return render(request, 'parents/index_parents.html', )


def add_parentssheet(request, token=None):
    request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
    s = URLSafeTimedSerializer(settings.SECRET_KEY)

    try:
        data = s.loads(token, max_age=7200) #Zeitangabe in Sekunden
        patient_uuid = data.get("patient_uuid")

        # Falls die UUID gültig ist, Formular anzeigen
        #return render(request, "fragebogen.html", {"patient_uuid": patient_uuid})
        if request.method == "POST":
            form = ParentsSheetFormStep1(request.POST)
            if form.is_valid():
                parents_item = form.save(commit=False)
                parents_item.save()
                logger.info('add_parentssheet')
                return redirect('/parents/index/')
        else:
            logger.debug('add_parentssheet: else')
            form = ParentsSheetFormStep1()
        return render(request, 'parents/parents_form.html', {'form': form})

    except SignatureExpired:
        return HttpResponse("Der Link ist abgelaufen.", status=410)
    except BadSignature:
        return HttpResponse("Ungültiger Link.", status=400)


def edit_parentssheet(request, id=None):
    request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
    item = get_object_or_404(Parents_sheet, id=id)
    form = ParentsSheetForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('Daten werden gespeichert')
        return redirect('/index/')
    logger.debug('edit_parentssheet')
    form.id = item.id
    return render(request, 'parents/parents_form.html', {'form': form})


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



