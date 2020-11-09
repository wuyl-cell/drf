import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelAdmin(object):
    pass


class CourseModelAdmin(object):
    pass


class TeacherModelAdmin(object):
    pass

class CourseChapterModelAdmin(object):
    pass

class CourseLessonModelAdmin(object):
    pass

xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)
xadmin.site.register(Course, CourseModelAdmin)
xadmin.site.register(Teacher, TeacherModelAdmin)
xadmin.site.register(CourseChapter, CourseChapterModelAdmin)
xadmin.site.register(CourseLesson, CourseLessonModelAdmin)