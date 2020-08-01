import os
import logging

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ParentsSheetForm
from .models import Parents_sheet

logger = logging.getLogger(__name__)


#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
    logger.info('Indexseite wurde geladen')
    #form = IndexForm()

    return render(request, 'parents/index_parents.html', )


def add_parentssheet(request):
    request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
    if request.method == "POST":
        form = ParentsSheetForm(request.POST)
        if form.is_valid():
            parents_item = form.save(commit=False)
            parents_item.save()
            logger.info('add_parentssheet')
            return redirect('/parents/parents/' + str(parents_item.id) + '/')
    else:
        logger.debug('add_parentssheet: else')
        form = ParentsSheetForm()
    return render(request, 'parents/parents_form.html', {'form': form})


def edit_parentssheet(request, id=None):
    request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
    item = get_object_or_404(Parents_sheet, id=id)
    form = ParentsSheetForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        logger.info('Daten werden gespeichert')
        return redirect('/parents/' + str(item.id) + '/')
    logger.debug('edit_parentssheet')
    form.id = item.id
    return render(request, 'parents/parents_form.html', {'form': form})
