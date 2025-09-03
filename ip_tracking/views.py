
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Middleware test OK")

# Create your views here.
