from django.conf import settings


class VariousHeaders(object):

    def process_response(self, request, response):
        response['X-XSS-Protection'] = '1; mode=block'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Security-Policy'] = 'upgrade-insecure-requests'
        return response
