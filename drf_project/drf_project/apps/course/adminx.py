import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson, CourseExpire, \
    CoursePriceDiscount, Activity, CourseDiscount, CourseDiscountType


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
xadmin.site.register(CourseExpire)
xadmin.site.register(CoursePriceDiscount)
xadmin.site.register(Activity)
xadmin.site.register(CourseDiscount)
xadmin.site.register(CourseDiscountType)