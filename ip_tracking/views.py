from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

# Anonymous users → 5 req/min, Authenticated users → 10 req/min
@ratelimit(key="ip", rate="5/m", method="ALL", block=True)
@ratelimit(key="user_or_ip", rate="10/m", method="ALL", block=True)
def login_view(request):
    return HttpResponse("Login successful (dummy view)")
