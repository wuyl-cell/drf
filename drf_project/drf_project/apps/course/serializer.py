from rest_framework import serializers

from course.models import CourseCategory, Course, Teacher


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['name', 'id']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name', 'id', 'title', 'signature']


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_img', 'students', 'lessons', 'pub_lessons', 'price'
                  , 'teacher', 'lesson_list']