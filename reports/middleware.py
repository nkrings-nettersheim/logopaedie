from django.core.exceptions import PermissionDenied
from django.conf import settings
from logopaedie.settings import X_FORWARD

from .models import Login_Failed

class IPAccessCheck:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        #self.ip_list = Login_Failed.objects.values_list('ipaddress', flat=True).distinct()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
        else:
            if X_FORWARD:
                ip_address = request.META.get('HTTP_X_FORWARDED_FOR')  # Get client IP address
            else:
                ip_address = request.META.get('REMOTE_ADDR')  # Get client IP address

            if Login_Failed.objects.filter(ipaddress=ip_address).count() > 5:
                raise PermissionDenied()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
