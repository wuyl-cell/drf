from rest_framework import serializers

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['name', 'id']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name', 'id', 'title', 'signature', 'image', 'brief']


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_img', 'students', 'lessons', 'pub_lessons', 'price'
                  , 'teacher', 'lesson_list', 'discount_name', 'real_price']


class CourseDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_img', 'students', 'lessons', 'pub_lessons', 'price',
                  'level_model', 'teacher', 'course_video', 'discount_name', 'real_price', 'active_time']


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'name', 'free_trail']


class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections = CourseLessonSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'chapter', 'name', 'coursesections']