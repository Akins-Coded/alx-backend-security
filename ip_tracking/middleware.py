import logging
import ipinfo
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.conf import settings
from .models import RequestLog, BlockedIP
from ipware import get_client_ip

ipinfo_handler = ipinfo.getHandler(settings.IPINFO_TOKEN)
logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip, is_routable = get_client_ip(request)
        ip_address = ip if ip else "0.0.0.0"

        # Check blacklist
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Forbidden: Your IP has been blocked.")

        # Check cache first
        geo_data = cache.get(ip_address)
        if not geo_data:
            try:
                details = ipinfo_handler.getDetails(ip_address)
                geo_data = {
                    "country": getattr(details, "country", None),
                    "city": getattr(details, "city", None),
                }
                cache.set(ip_address, geo_data, 60 * 60 * 24)  # cache for 24h
            except Exception:
                geo_data = {"country": None, "city": None}

        # Log request in DB
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path,
            country=geo_data["country"],
            city=geo_data["city"],
        )

        # Log to console/file
        logger.info(
            f"Request from {ip_address} ({geo_data['country']}, {geo_data['city']}) at {request.path}"
        )

        return self.get_response(request)
