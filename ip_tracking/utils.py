def user_or_ip(request):
    if request.user.is_authenticated:
        # Use user ID for authenticated users
        return str(request.user.id)
    # Use IP for anonymous users
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
