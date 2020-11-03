import jwt
from rest_framework import exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler


class JWTAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
        print(jwt_token)
        token = self.parse_jwt_token(jwt_token)
        if token is None:
            return None
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('签名已过期')
        except:
            raise exceptions.AuthenticationFailed('非法用户')

        user = self.authenticate_credentials(payload)
        return user, token

    def parse_jwt_token(self,jwt_token):
        token = jwt_token.split()
        if len(token) != 3 or token[0].lower() != 'auth' or token[2].lower() != 'jwt':
            return None
        return token[1]