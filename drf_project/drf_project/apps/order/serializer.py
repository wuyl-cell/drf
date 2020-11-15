from datetime import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from course.models import Course, CourseExpire
from order.models import Order, OrderDetail


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'pay_type')

        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'order_number': {
                'read_only': True
            },
            'pay_type': {
                'write_only': True
            },
        }

        def validate_pay_type(self, pay_type):
            try:
                Order.pay_choices[pay_type]
            except Order.DoesNotExist:
                raise serializers.ValidationError('当前的支付方式不允许！')

            return pay_type

        def create(self, validated_data):
            redis_connection = get_redis_connection('cart')

            # user_id = self.context['request'].user.id.
            user_id = 1
            incr = redis_connection.incr('number')

            # 生成订单号
            order_number = datetime.now().timestamp() + '%06d' % user_id + '%06d' % incr

            # 生成一个空订单
            order = Order.objects.create(
                order_title='课程订单',
                total_price=0,
                real_price=0,
                order_number=order_number,
                order_status=0,
                pay_type=validated_data.get('pay_type'),
                credit=0,
                coupon=0,
                order_desc='开开心心购物，哈哈哈哈哈哈',
                user=user_id
            )

            cart_list = redis_connection.hgetall('cart_%s', user_id)
            selected_list = redis_connection.smember('selected_%s', user_id)

            # 获取购物车中被勾选的商品
            for cart_id_byte, expire_id_byte in cart_list.items:
                cart_id = int(cart_id_byte)
                expire_id = int(expire_id_byte)
                # 判断是否被勾选
                if cart_id_byte in selected_list:
                    try:
                        course = Course.objects.get(id=cart_id, is_delete=False, is_show=True)
                    except Course.DoesNotExist:
                        raise serializers.ValidationError('对不起，你所购买的课程不存在')

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

                    try:
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=origin_price,
                            real_price=final_price,
                            discount_name=course.discount_name
                        )
                    except:
                        raise serializers.ValidationError("订单生成失败")

                    order.origin_price += float(origin_price)
                    order.final_price += float(final_price)
                    order.save()

            return order


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number", "pay_type")

        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},
        }

    def validate_pay_type(self, pay_type):
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError('当前的支付方式不允许！')

        return pay_type

    @transaction.atomic()
    def create(self, validated_data):
        redis_connection = get_redis_connection('cart')

        user_id = self.context['request'].user.id
        incr = redis_connection.incr('number')

        # 生成订单号
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr

        # 生成一个空订单
        order = Order.objects.create(
            order_title='课程订单',
            total_price=0,
            real_price=0,
            order_number=order_number,
            order_status=0,
            pay_type=validated_data.get('pay_type'),
            credit=0,
            coupon=0,
            order_desc='开开心心购物，哈哈哈哈哈哈',
            user_id=user_id
        )

        cart_list = redis_connection.hgetall('cart_%s' % user_id)
        selected_list = redis_connection.smembers('selected_%s' % user_id)

        # 获取购物车中被勾选的商品
        for cart_id_byte, expire_id_byte in cart_list.items():
            cart_id = int(cart_id_byte)
            expire_id = int(expire_id_byte)
            # 判断是否被勾选
            if cart_id_byte in selected_list:
                try:
                    course = Course.objects.get(id=cart_id, is_delete=False, is_show=True)
                except Course.DoesNotExist:
                    raise serializers.ValidationError('对不起，你所购买的课程不存在')

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

                try:
                    OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_id,
                        price=origin_price,
                        real_price=final_price,
                        discount_name=course.discount_name
                    )
                except:
                    raise serializers.ValidationError("订单生成失败")

                order.total_price += float(origin_price)
                order.real_price += float(final_price)
                order.save()

                redis_connection.hdel('cart_%s' % user_id, cart_id)
                redis_connection.srem('selected_%s' % user_id, cart_id)

        return order
