from django.urls import path

from api import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('test/', views.Test.as_view()),
    path('phone/', views.PhoneView.as_view()),

]