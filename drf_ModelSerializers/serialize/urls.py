from django.urls import path

from serialize import views

urlpatterns = [
    path('TeacherAPI/', views.TeacherAPI.as_view()),
    path('TeacherAPI/<str:id>', views.TeacherAPI.as_view())
]