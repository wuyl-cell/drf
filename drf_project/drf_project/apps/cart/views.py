from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ViewSet

from cart.utils import get_car_len, get_all_status
from course.models import Course, CourseExpire
from drf_project.utils import contastnt

redis_connection = get_redis_connection('cart')


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    # post请求  用于给购物车添加商品
    def add_cart(self, request):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        select = True
        expire = 0

        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)

        except Course.DoesNotExist:
            return Response({'message': '参数有误，课程不存在！'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # pipeline一次可以对redis进行多条数据操作
            pipeline = redis_connection.pipeline()
            # 对课程的信息及有效期进行存储(使用的是hash存储)
            pipeline.hset('cart_%s' % user_id, course_id, expire)
            # 对课程是否勾选进行存储(使用的是集合进行存储)
            # pipeline.sadd('selected_%s' % user_id, course_id)
            pipeline.execute()
            course_len = redis_connection.hlen('cart_%s' % user_id)
            return Response({'message': '加入购物车成功', 'cart_len': course_len})
        except:
            return Response({'message': '添加购物车失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    # get请求，用于获取购物车中的信息
    def car_list(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        cart_list_bytes = redis_connection.hgetall('cart_%s' % user_id)
        selected_list_bytes = redis_connection.smembers('selected_%s' % user_id)
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
                data.append({
                    'selected': True if course_id_byte in selected_list_bytes else False,
                    'course_img': contastnt.IMG_SRC + course.course_img.url,
                    'name': course.name,
                    'real_price': course.real_price,
                    'price': course.price,
                    'id': course.id,
                    'expire_list': course.expire_text,
                    'expire_id': expire_id
                })
            except Course.DoesNotExist:
                continue
        course_len = get_car_len(user_id)
        return Response({'data': data, 'cart_len': course_len})

    # patch请求，用于改变商品的选中状态（全选还有问题）
    def check_status(self, request):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        try:
            selected_item = redis_connection.smembers('selected_%s' % user_id)
            flag = True
            for i in selected_item:
                if int(course_id) == int(i.decode()):
                    flag = False
                    redis_connection.srem('selected_%s' % user_id, course_id)
            if flag:
                redis_connection.sadd('selected_%s' % user_id, course_id)
            return Response({'修改成功'})
        except:
            return Response({'修改失败，请稍后再试'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        

    # delete请求，用于从购物车删除单个商品和多个商品
    def delete_item(self, request):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        if course_id:
            try:
                redis_connection.hdel('cart_%s' % user_id, course_id)
                redis_connection.srem('selected_%s' % user_id, course_id)
                course_len = redis_connection.hlen('cart_%s' % user_id)
                return Response({'message': '删除成功', 'cart_len': course_len})
            except:
                return Response({'message': '出错了，删除失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        else:
            try:
                selected_list_bytes = redis_connection.smembers('selected_%s' % user_id)
                for id in selected_list_bytes:
                    course_id = id.decode()
                    redis_connection.hdel('cart_%s' % user_id, course_id)
                redis_connection.delete('selected_%s' % user_id)
                course_len = redis_connection.hlen('cart_%s' % user_id)
            except:
                return Response({'message': '出错了，删除失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
            return Response({'message': '删除成功', 'cart_len': course_len})

    # put请求，用于修改商品的有效期
    def change_expire(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        expire_id = request.data.get('expire_id')

        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except Course.DoesNotExist:
            return Response({'message': '图书不存在'}, status=status.HTTP_400_BAD_REQUEST)

        ex_id = CourseExpire.objects.filter(id=expire_id)
        if not ex_id and expire_id != 0:
            return Response({'message': '有效期类型错误'}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection.hset('cart_%s' % user_id, course_id, expire_id)
        return Response({'message': '课程有效期修改成功'})

    # get请求，用于在订单页面显示商品信息
    def get_select_course(self, request):
        user_id = request.user.id
        #获取redis数据库中的数据
        cart_list = redis_connection.hgetall('cart_%s' % user_id)
        select_list = redis_connection.smembers('selected_%s'%user_id)
        data = []
        total_price = 0
        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            if course_id_byte in select_list:
                try:
                    course = Course.objects.get(is_delete=False, is_show=True, id=course_id)
                except Course.DoesNotExist:
                    continue
                origin_price = course.price
                expire_text = '永久有效'
                final_price = course.real_price
                if expire_id > 0:
                    try:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        origin_price = course_expire.price
                        expire_text = course_expire.expire_text
                        for expire in course.expire_text:
                            if int(expire_id) == int(expire.get('expire_id')):
                                final_price = expire.get('price')
                    except:
                        continue

                data.append({
                    'course_img': contastnt.IMG_SRC + course.course_img.url,
                    'name': course.name,
                    'final_price': final_price,
                    'price': origin_price,
                    'id': course.id,
                    'expire_text': expire_text
                })

                total_price += final_price

        return Response({'course_list': data, 'total_price': total_price, 'message': '获取成功'})


class InitStatus(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        data = get_all_status(user_id)
        return Response(data)
