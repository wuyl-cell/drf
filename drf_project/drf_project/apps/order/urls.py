from django.urls import path

from order import views

urlpatterns = [
    path('create_order/', views.OrderAPIView.as_view())
]