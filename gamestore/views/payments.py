"""
Selled ID: 57b91FDFa2Sy
Secret Key: 873efc3f8f8ca2605de7a4101d3322ba
API:http://payments.webcourse.niksula.hut.fi/
POST http://payments.webcourse.niksula.hut.fi/pay/
"""
from django.http import HttpResponse


def success(request):
    return HttpResponse()


def cancel(request):
    return HttpResponse()


def error(request):
    return HttpResponse()
