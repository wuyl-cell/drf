from django.contrib import admin

# Register your models here.
from first import models

admin.site.register(models.User)
admin.site.register(models.Teacher)
admin.site.register(models.Department)
