from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.utils import get_car_len
from home.models import Banner, Nav
from home.serializer import BannerSerializer, NavSerializer


class BannerList(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    serializer_class = BannerSerializer


class HeaderList(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=True).order_by('-orders')
    serializer_class = NavSerializer


class FooterList(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=False).order_by('-orders')
    serializer_class = NavSerializer


class GetCartLen(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cart_len = get_car_len(user_id)
        return Response({'cart_len': cart_len})