from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from first.models import Teacher
from first.serializers import TeacherSerializer, TeacherDeSerializer, TeacherModelSerializer


@csrf_exempt
def user(request):
    if request.method == "POST":
        return HttpResponse('post ok')
    else:
        return HttpResponse('get ok')
 

# 类视图
@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('UserView get ok')

    def post(self, request, *args, **kwargs):
        return HttpResponse('UserView post ok')


class TeacherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            res = Teacher.objects.filter(pk=id)
            result = TeacherSerializer(res, many=True).data
            return Response({
                'status': 200,
                'message': '查询单个',
                'result': result
            })
        else:
            res = Teacher.objects.all()
            result = TeacherSerializer(res, many=True).data
            return Response({
                'status': 200,
                'message': '查询全部',
                'result': result
            })

    def post(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, dict or data == {}):
            return Response({
                'status': 400,
                'message': '参数有误'
            })
        se_data = TeacherDeSerializer(data=data)
        if se_data.is_valid():
            teacher = se_data.save()
            print(teacher)
            return Response({
                'status': 200,
                'message': '插入单个',
                'result': TeacherSerializer(teacher).data
            })
        else:
            return Response({
                'status': 400,
                'message': '员工添加失败',
                'results': se_data.errors
            })


class TeacherAPI(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            teacher = Teacher.objects.get(pk=id)
            return Response(
                {
                    'status': 200,
                    'message': '查询单个成功',
                    'result': TeacherModelSerializer(teacher).data
                }
            )
        else:
            return Response('错误')

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        return Response('post ok')


