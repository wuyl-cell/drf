from django.urls import path
from rest_framework import request
from drf_day5 import views

urlpatterns = [
    path('test/', views.Test.as_view())
]