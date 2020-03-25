from django.core.exceptions import PermissionDenied
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
            # Do something for authenticated users.
            ...
        else:
            ip_check_list = []
            ip = request.META.get('REMOTE_ADDR')  # Get client IP address
            ip_list = Login_Failed.objects.values_list('ipaddress', flat=True).distinct()
            for ip in ip_list:
                ip_count = Login_Failed.objects.filter(ipaddress=ip).count()
                if ip_count > 5:
                    ip_check_list.append(ip)

            if ip in ip_check_list:
                raise PermissionDenied()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
