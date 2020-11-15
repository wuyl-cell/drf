import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import User
from user.utils import get_use_by_account


class UserSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text='用户token')
    code = serializers.CharField(max_length=1024, write_only=True, help_text='短信验证码')
    class Meta:
        model = User
        fields = ['phone', 'password', 'username', 'token', 'code']
        extra_kwargs = {
            'phone': {
                'write_only': True
            },
            'password': {
                'write_only': True
            },
            'username': {
                'read_only': True
            }
        }

    def validate_phone(self, phone):

        if not re.match(r'^[1][3,4,5,7,8][0-9]{9}$', phone):
            raise serializers.ValidationError('手机号格式不正确')

        try:
            user = get_use_by_account(phone)
        except User.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError('手机号已经被注册')

        return phone

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError('密码必须大于六位数')
        if password.isalpha() or password.isdigit():
            raise serializers.ValidationError('密码必须是数字和字母的混合')
        return password

    def validate(self, attr):
        code = attr.get('code')
        phone = attr.get('phone')
        redis_connect = get_redis_connection('sms_code')
        code_right = redis_connect.get('mobile_%s' % phone)

        if (code_right).decode() == code:
            return attr
        raise serializers.ValidationError('验证码错误')


    def create(self, validated_data):
        phone = validated_data.get('phone')
        password = validated_data.get('password')

        username = phone

        user = User.objects.create(
            phone=phone,
            username=username,
            password=make_password(password)
        )
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user
