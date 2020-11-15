from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import CourseCategory, Course, CourseChapter
from course.pagination import MyPagination
from course.serializer import CourseCategorySerializer, CourseSerializer, CourseDetailSerializer, \
    CourseChapterSerializer


class CourseCategoryList(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseCategorySerializer


class CourseList(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    #查询的条件
    filter_fields =('course_category', )

    #排序的条件
    ordering_fields =('id', 'price', 'students')

    #指定分页类
    pagination_class = MyPagination


class CourseDetail(RetrieveAPIView):
    queryset = Course.objects.filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseDetailSerializer


class CourseLessons(ListAPIView):
    queryset = CourseChapter.objects.filter(is_delete=False, is_show=True).order_by('id')
    serializer_class = CourseChapterSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']