from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class  User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'api_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Telephone(models.Model):
    com_name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    memory = models.IntegerField()
    brand = models.CharField(max_length=20)

    class Meta:
        db_table = 'api_phone'
        verbose_name = '手机'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.com_name