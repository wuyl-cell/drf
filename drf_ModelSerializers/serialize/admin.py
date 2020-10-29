from django.contrib import admin

# Register your models here.
from serialize.models import Teacher, Department

admin.site.register(Teacher)
admin.site.register(Department)