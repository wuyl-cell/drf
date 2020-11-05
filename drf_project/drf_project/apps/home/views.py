from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.generics import ListAPIView

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