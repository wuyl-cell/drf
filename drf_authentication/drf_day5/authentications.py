from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from drf_day5.models import User


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', None)

        if auth is None:
            return None

        auth_split = auth.split()
        if not (len(auth_split) == 2 and auth_split[0].lower() == 'auth'):
            raise exceptions.AuthenticationFailed('认证信息有误，认证失败')

        if auth_split[1] != 'abc.admin.123':
            raise exceptions.AuthenticationFailed('用户信息认证失败')
        user = User.objects.filter(username='admin').first()
        if not user:
            raise exceptions.AuthenticationFailed('用户不存在或已被删除')

        return user, None