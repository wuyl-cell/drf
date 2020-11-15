from django.urls import path

from course import views

urlpatterns = [
    path('category_list/', views.CourseCategoryList.as_view()),
    path('course_list/', views.CourseList.as_view()),
    path('course_detail/<str:pk>/', views.CourseDetail.as_view()),
    path('course_lessons/', views.CourseLessons.as_view()),
]