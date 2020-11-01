import mixins as mixins
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
from drf_day4.models import Book, User
from drf_day4.serializers import BookModelSerializerV2, BookModelSerializerV3, UserModelSerializer


class BookView(APIView):
    def get(self, request, *args, **kwargs):

        return Response('ok')
    #群体修改(需要在序列化类的Meta类中添加list_serializer_class = BookListSerializer)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id]
            request_data = [request_data]
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            for dic in request_data:
                pk = dic.pop('id', None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': '参数中缺少书的id',
                    })
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': '参数格式错误',
            })
        book_list = []
        new_data = []
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
            except Book.DoesNotExist:
                continue
        se_book = BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        se_book.is_valid(raise_exception=True)
        se_book.save()

        return Response({
            'status': status.HTTP_200_OK,
            'message': '修改成功',
        })


class BookGenericAPIView(GenericAPIView,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.UpdateModelMixin):
    queryset = Book.objects.filter()
    serializer_class = BookModelSerializerV3
    lookup_field = 'id'
    #只继承了GenericAPIView的写法

    # 查询所有的书
    # def get(self, request, *args, **kwargs):
    #     book_list = self.get_queryset()
    #     se_data = self.get_serializer(book_list, many=True)
    #     return Response({
    #         'status': status.HTTP_200_OK,
    #         'message': '查询所有的书',
    #         'result': se_data.data
    #     })

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserViewSetViewRegister(viewsets.ViewSet):
    def user_register(self, request, *args, **kwargs):
        data = request.data
        re_data = UserModelSerializer(data=data)
        re_data.is_valid(raise_exception=True)
        re_data.save()
        return Response('注册成功')

class UserViewSetView(viewsets.ViewSet):
    def user_login(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        try:
            res = User.objects.get(username=username)

            if res.password == password:
                data = UserModelSerializer(res).data
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': '登陆成功',
                    'result': data
                })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': '密码错误'
                })
        except:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': '用户名不存在'
            })