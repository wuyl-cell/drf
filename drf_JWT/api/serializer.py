import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from api.models import User, Telephone


class UserSerializer(ModelSerializer):
    account = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['account', 'password', 'username', 'email', 'phone']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'password': {
                'read_only': True
            },
            'phone': {
                'read_only': True
            },
        }

    def validate(self, attrs):
        account = attrs.get('account')
        password = attrs.get('password')
        msg = 'User account is disable'
        if re.match(r'1[3,5,7,8,9][0-9]{9}', account):
            res = User.objects.filter(phone=account).first()
        elif re.match(r'.+@.+', account):
            res = User.objects.filter(email=account).first()
        else:
            res = User.objects.filter(username=account).first()
        if res and res.check_password(password):
            payload = jwt_payload_handler(res)
            token = jwt_encode_handler(payload)
            self.token = token
            self.user = res
        else:
            raise serializers.ValidationError(msg)
        return attrs

class PhoneSerializer(ModelSerializer):


    class Meta:
        model = Telephone
        fields = ['com_name', 'price', 'brand']