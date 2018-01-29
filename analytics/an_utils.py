def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def is_bot(request):
    botnames = ['Googlebot', 'Slurp', 'Twiceler', 'msnbot', 'KaloogaBot', 'YodaoBot', '"Baiduspider', 'googlebot',
                'Speedy Spider', 'DotBot']
    user_agent = request.META.get('HTTP_USER_AGENT', None)

    for botname in botnames:
        if botname in user_agent:
            return True
        else:
            return False
