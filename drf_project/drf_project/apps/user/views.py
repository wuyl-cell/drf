from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as drf_status
from rest_framework_jwt.settings import api_settings

from drf_project.libs.geetest import GeetestLib
from drf_project.utils.contastnt import SMS_EXPIRE_TIME, CODE_EXPIRE_TIME, API_KEY
from drf_project.utils.send_message import Message
from user.models import User
from user.serializer import UserSerializer
from user.utils import get_use_by_account, random_code
from rest_framework.generics import CreateAPIView, GenericAPIView

pc_geetest_id = "1ea3ed8b35299a931b6a3883ec4a05be"
pc_geetest_key = "9a13879615c1ae2500e356417cd5bcf9"
redis_connect = get_redis_connection('sms_code')


#获取滑块验证码
class Captcha(APIView):
    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        user = get_use_by_account(username)
        if user is None:
            return Response({'message': '用户不存在'}, status=drf_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')

        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


#注册
class RegisterView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        redis_connect.delete('sms_%s' % phone, )
        redis_connect.delete('mobile_%s' % phone, )
        return Response(serializer.data, status=drf_status.HTTP_200_CREATED)


#注册之前对手机号进行校验
class CheckPhoneRegister(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        user = get_use_by_account(phone)
        if user:
            return Response({'message': '手机号已被注册'}, status=drf_status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'ok'})


#用短信登陆发送验证码之前对手机号进行校验
class CheckPhoneLogin(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        print('phone ='+phone)
        user = get_use_by_account(phone)
        if user:
            return Response({'message': 'ok'})
        else:
            return Response({'message': '手机号还未被注册，请先注册'}, status=drf_status.HTTP_400_BAD_REQUEST)


#用短信登陆
class MessageLogin(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        code = request.query_params.get('code')
        code_right = redis_connect.get('mobile_%s' % phone)
        if (code_right).decode() == code:
            user = get_use_by_account(phone)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.token = token
            redis_connect.delete('sms_%s' % phone, )
            redis_connect.delete('mobile_%s' % phone, )
            return Response({
                'token': token,
                'user': user.username,
                'user_id': user.id,
            })
        else:
            return Response({'message': '验证码错误'}, status=drf_status.HTTP_400_BAD_REQUEST)


#发送验证码
class SendMessage(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')



        #判断60秒内是否发送过验证码
        mobile_code = redis_connect.get('sms_%s' % phone)
        if mobile_code:
            return Response({'message': '60秒内已经发送给验证码'}, status=drf_status.HTTP_400_BAD_REQUEST)

        #生成验证码
        code = random_code()

        #将数据存到redis数据库
        redis_connect.setex('sms_%s' % phone, SMS_EXPIRE_TIME, code)
        redis_connect.setex('mobile_%s' % phone, CODE_EXPIRE_TIME, code)

        #发送验证码
        try:
            message = Message()
            message.send_message(phone, code)
        except:
            return Response({'message': '验证码发送失败'}, status=drf_status.HTTP_500_BAD_REQUEST)

        return Response({'message': '验证码发送成功'}, status=drf_status.HTTP_200_OK)






