from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

from .utils import user_or_ip


@csrf_exempt  # only if you’re testing login without CSRF tokens
@ratelimit(key=user_or_ip, rate='5/m', method='ALL', block=True)
@ratelimit(key='user', rate='10/m', method='ALL', block=True)
def login_view(request):
    """
    Rate limits:
        - Authenticated users: 10 requests/min
        - Anonymous users: 5 requests/min
    """
    return HttpResponse("Coded Login successful (Real view)")
