from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('captcha/', views.Captcha.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('phone_register/', views.CheckPhoneRegister.as_view()),
    path('phone_login/', views.CheckPhoneLogin.as_view()),
    path('get_code/', views.SendMessage.as_view()),
    path('message_login/', views.MessageLogin.as_view()),
]