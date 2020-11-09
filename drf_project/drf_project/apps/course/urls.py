from django.urls import path

from course import views

urlpatterns = [
    path('category_list/', views.CourseCategoryList.as_view()),
    path('course_list/', views.CourseList.as_view()),
]