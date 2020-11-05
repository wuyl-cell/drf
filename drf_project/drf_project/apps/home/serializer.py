from rest_framework import serializers

from home.models import Banner, Nav


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
         model = Banner
         fields = ['img', 'link']


class NavSerializer(serializers.ModelSerializer):
    class Meta:
         model = Nav
         fields = ['title', 'link', 'position', 'is_site']