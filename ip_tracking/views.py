from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from .utils import user_or_ip

@ratelimit(key='user_or_ip', rate='10/m', method='ALL', block=True)
def login_view(request):
    """
    Rate limits:
        - Authenticated users: 10 requests/min
        - Anonymous users: 5 requests/min (handled inside user_or_ip)
    """
    return HttpResponse("Coded Login successful (dummy view)")
