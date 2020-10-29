from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from serialize.models import Teacher
from serialize.serializers import TeacherModelsSerializers


class TeacherAPI(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            try:
                teacher = Teacher.objects.get(pk=id)
            except:
                return Response({
                    'status': 400,
                    'message': 'id错误'
                })
            return Response({
                'status': 200,
                'message': '查询单个成功',
                'result': TeacherModelsSerializers(teacher).data
            })
        else:
            teachers = Teacher.objects.filter(is_delete=False)
            return Response({
                'status': 200,
                'message': '查询所有',
                'result': TeacherModelsSerializers(teachers, many=True).data
            })

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        if isinstance(data, dict):
            many = False
        elif isinstance(data, list):
            many = True
        else:
            return Response({
                'status': 400,
                'message': '参数有误',
            })
        re_data = TeacherModelsSerializers(data=data, many=many)
        re_data.is_valid(raise_exception=True)
        obj = re_data.save()
        return Response({
            'status': 200,
            'message': '添加图书成功',
            'results': TeacherModelsSerializers(obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id:
            ids = [id]
        else:
            ids = request.data.get('ids')
        response = Teacher.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                'status': 200,
                'message': '删除成功'
            })
        return Response({
            'status': 400,
            'message': '删除失败或存在'
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        id = kwargs.get('id')
        try:
            obj = Teacher.objects.get(pk=id)
        except Teacher.DoesNotExist:
            return Response({
                'status': 400,
                'message': '不存在'
            })
        se_data = TeacherModelsSerializers(data=request_data, instance=obj)
        se_data.is_valid(raise_exception=True)
        se_data.save()
        return Response({
            'status': 200,
            'message': '修改成功',
            'results': TeacherModelsSerializers(obj).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        id = kwargs.get("id")
        try:
            obj = Teacher.objects.get(pk=id)
        except Teacher.DoesNotExist:
            return Response({
                'status': 400,
                'message': '不存在'
            })

        se_data = TeacherModelsSerializers(data=request_data, instance=obj, partial=True)
        se_data.is_valid(raise_exception=True)
        se_data.save()
        return Response({
            "status": 200,
            "message": '修改成功',
            "results": TeacherModelsSerializers(obj).data
        })