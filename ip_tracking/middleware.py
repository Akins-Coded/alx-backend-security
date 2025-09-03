import logging
from django.utils.timezone import now
from .models import RequestLog
from ipware import get_client_ip 

logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip, is_routable = get_client_ip(request)
        ip_address = ip if ip else "0.0.0.0" # Avoid failing

        # Save request details
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path,
        )

        # Debug log
        logger.info(f"Request from {ip_address} at {request.path}")

        return self.get_response(request)
