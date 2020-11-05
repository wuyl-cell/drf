from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.authentication import JWTAuthentication
from api.filter import PhoneFilter
from api.models import Telephone
from api.page import MyPageNumberPagination, MyLimitOffsetPagination
from api.serializer import UserSerializer, PhoneSerializer


class Login(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'token': serializer.token,
            'user': UserSerializer(serializer.user).data
        }
        return Response(data)


class Test(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response('验证通过')


class PhoneView(ListAPIView):
    queryset = Telephone.objects.all()
    serializer_class = PhoneSerializer

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # search_fields = ['com_name', 'price']
    # ordering = ['price']
    pagination_class = MyPageNumberPagination
    # filter_class = PhoneFilter