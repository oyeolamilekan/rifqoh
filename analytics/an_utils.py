import requests

# Get user current location
def get_location(request=None,number=None):
    if request:
        user_ip = get_client_ip(request)
        get_user_info = requests.get('http://freegeoip.net/json/{}'.format(user_ip)).json()
        user_country_code = get_user_info['country_code']
        user_country_name = get_user_info['country_name']
    else:
        get_user_info = requests.get('http://freegeoip.net/json/{}'.format(number)).json()
        user_country_code = get_user_info['country_code']
        user_country_name = get_user_info['country_name']
    return user_country_name, user_country_code

# Get the Ip address of the user
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip

# Get header info
def get_header_info(request):
    user_header = request.META.get('HTTP_USER_AGENT',None)
    return user_header


# Checks if the request is robot and it is, it doesn't add it to the database.
def is_bot(request):
    botnames = ('Googlebot', 'Slurp', 'Twiceler', 'msnbot', 'KaloogaBot', 'YodaoBot', 'Baiduspider', 'googlebot',
                'Speedy Spider', 'DotBot','robot','bots','Mediapartners-Google','robot','Python-urllib',
                'python-requests','YandexBot','Twitterbot','Trident','LinkedInBot','muhstik','OpenLinkProfiler.org',
                'bingbot','DuckDuckGo','Trident','libwww-perl','zgrab')

    user_agent = request.META.get('HTTP_USER_AGENT', None)
    tested = None
    for bot in botnames:
        num = user_agent.find(bot)

        if num != -1:
            tested = True
            return True
            break
    if not tested:
        return False