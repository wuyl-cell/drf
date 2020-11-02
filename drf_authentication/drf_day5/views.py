from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_day5.authentications import MyAuth
from drf_day5.permission import MyPermission
from drf_day5.throttle import SendMessageRate


class Test(APIView):
    authentication_classes = [MyAuth]
    permission_classes = [MyPermission]
    throttle_classes = [SendMessageRate]

    def get(self, request, *args, **kwargs):
        return Response('ok')

    def post(self, request, *args, **kwargs):
        return Response('post ok')
