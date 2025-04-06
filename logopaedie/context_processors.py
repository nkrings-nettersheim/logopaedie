#context_processors.py
from django.conf import settings

def static_version(request):
    return {
        'STATIC_VERSION': settings.STATIC_VERSION
    }

def app_version(request):
    return {
        'APP_VERSION': settings.APP_VERSION
    }