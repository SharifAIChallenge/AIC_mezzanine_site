from pygeoip import GeoIP

class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        geo_ip = GeoIP('geoip.dat')
        ip = request.META.get('REMOTE_ADDR', None) or request.META.get('HTTP_X_REAL_IP', None)
        if ip:
            if ip.startswith("213.233."):
                country_code = 'IR'
            else:
                country_code = geo_ip.country_code_by_name(ip)
        else:
            country_code = 'IR'
        if country_code == 'IR':
            if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
                del request.META['HTTP_ACCEPT_LANGUAGE']
