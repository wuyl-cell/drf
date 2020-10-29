from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    status = models.CharField(max_length=12, default='活跃')

    class Meta:
        abstract = True


class User(models.Model):
    gender_choices = (
        (0, 'male'),
        (1, 'famale'),
        (2, 'other'),
    )
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)

    class Meta:
        db_table = 'user_brf'

    def __str__(self):
        return self.username


class Department(models.Model):
    de_name = models.CharField(max_length=20)
    people_num = models.IntegerField()

    class Meta:
        db_table = 'department_drf'
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.de_name




class Teacher(models.Model):
    gender_choices = {
        (0, 'male'),
        (1, 'famale'),
        (2, 'other')
    }
    name = models.CharField(max_length=20)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)

    class Meta:
        db_table = 'teacher_brf'
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def de_name(self):
        return self.department.de_name

    @property
    def gender1(self):
        return self.get_gender_display()



