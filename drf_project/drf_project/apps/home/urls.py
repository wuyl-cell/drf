from django.urls import path

from home import views

urlpatterns = [
    path('banner/', views.BannerList.as_view()),
    path('header/', views.HeaderList.as_view()),
    path('footer/', views.FooterList.as_view()),
    path('cart_len/', views.GetCartLen.as_view()),
]