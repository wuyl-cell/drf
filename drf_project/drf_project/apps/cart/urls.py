from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartViewSet.as_view({'post': 'add_cart', 'get': 'car_list', 'patch': 'check_status', 'delete':'delete_item', 'put': 'change_expire'})),
    path('order_info/', views.CartViewSet.as_view({'get': 'get_select_course'})),
    path('status/', views.InitStatus.as_view()),
]