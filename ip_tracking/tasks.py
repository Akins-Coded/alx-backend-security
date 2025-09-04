from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from .models import SuspiciousIP

SENSITIVE_PATHS = ["/admin", "/login"]

@shared_task
def detect_suspicious_ips():
    """
    Celery task to detect suspicious IPs from Redis logs.
    Runs hourly.
    """
    # Keys set by middleware look like: ip:{ip}
    keys = cache.keys("ip:*")

    for key in keys:
        ip_data = cache.get(key)
        if not ip_data:
            continue

        ip_address = key.split(":")[1]
        count = ip_data.get("count", 0)
        paths = ip_data.get("paths", [])

        reasons = []

        # Rule 1: High request rate
        if count > 100:
            reasons.append(f"Excessive requests: {count} in last hour")

        # Rule 2: Accessing sensitive paths
        for path in paths:
            if any(path.startswith(sp) for sp in SENSITIVE_PATHS):
                reasons.append(f"Accessed sensitive path: {path}")

        # Save suspicious IPs
        for reason in reasons:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip_address,
                reason=reason,
            )

    return f"Checked {len(keys)} IPs at {timezone.now()}"
