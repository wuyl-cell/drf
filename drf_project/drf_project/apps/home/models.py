from django.db import models

# Create your models here.
from home.basemodel import BaseModel


class Banner(BaseModel):
    img = models.ImageField(upload_to="banner", max_length=255, verbose_name="轮播图")
    title = models.CharField(max_length=200, verbose_name="图片标题")
    link = models.CharField(max_length=300, verbose_name="图片链接")

    class Meta:
        db_table = "banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Nav(BaseModel):
    position_option = (
        (1, '顶部导航'),
        (0, '底部导航'),
    )

    title = models.CharField(max_length=200, verbose_name='导航标题')
    link = models.CharField(max_length=300, verbose_name='导航链接')
    position = models.BooleanField(choices=position_option, default=1, verbose_name='导航位置')
    is_site = models.BooleanField(default=1, verbose_name='是否是站外的链接')
    class Meta:
        db_table = "nav"
        verbose_name = "导航栏"
        verbose_name_plural = verbose_name