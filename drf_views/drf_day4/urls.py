from django.urls import path

from drf_day4 import views

urlpatterns = [
    path('book/', views.BookView.as_view()),
    path('book/<str:id>', views.BookView.as_view()),
    path('bookGeneric/', views.BookGenericAPIView.as_view()),
    path('bookGeneric/<str:id>', views.BookGenericAPIView.as_view()),
    path('userViewSet/', views.UserViewSetViewRegister.as_view({'post':'user_register'})),
    path('userViewSetlogin/', views.UserViewSetView.as_view({'post':'user_login'})),
    path('userViewSet/<str:id>', views.UserViewSetViewRegister.as_view({'post':'user_register'})),
]

