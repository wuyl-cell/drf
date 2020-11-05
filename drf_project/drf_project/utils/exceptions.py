from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    error = '%s,%s,%s' % (context['view'], context['request'].method, exc)
    print(error)
    response =  drf_exception_handler(exc, context)
    if response is None:
        return Response({'error_message': '异常正在处理中'})