from rest_framework import serializers

from drf_day4.models import Book, Press, User


class BookListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成更新多个对象
    """

    # 重写update方法完成更新
    def update(self, instance, validated_data):
        print(instance)  # 要修改的实例
        print(validated_data)  # 要修改的实例的值
        print(self.child)  # 调用逻辑的序列化器类-->BookModelSerializerV2

        # TODO 将修改多个  改变成循环中每次修改一个
        for index, obj in enumerate(instance):
            # 每遍历一次  就修改一个对象的数据
            self.child.update(obj, validated_data[index])

        return instance


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields应该写哪些字段  应该填写序列化与反序列化所需字段的并集
        fields = ("book_name", "price", "publish", "authors", "pic")

        list_serializer_class = BookListSerializer

        extra_kwargs = {
            "book_name": {
                "required": True,  # 必填字段
                "min_length": 2,  # 最小长度
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            },
            # 指定某个字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
        }

    # def validate(self, attrs):
    #     # print(attrs)
    #     return attrs
    #
    # def validate_book_name(self, obj):
    #     # print(obj)
    #     return obj

    # def update(self, instance, validated_data):
    #     book_name = validated_data.get("book_name")
    #     instance.book_name = book_name
    #     instance.save()
    #     return instance


class BookModelSerializerV3(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors", "pic", 'author_list')

        extra_kwargs = {
            "book_name": {
                "required": True,  # 必填字段
                "min_length": 2,  # 最小长度
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            },
            # 指定某个字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
            'author_list': {
                'read_only': True
            }
        }


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'gender', 'gender1', 'age', 're_pwd')
        extra_kwargs = {
            'username': {
                'required': True,
                'max_length': 20,
                'min_length': 2,
                'error_messages': {
                    'max_length': '用户名太短',
                    'min_length': '用户名太长',
                    'required': '用户名必须提供'
                }
            },
            'gender': {
                "write_only": True
            },
            'gender1': {
                "read_only": True
            },
            're_pwd': {
                "write_only": True
            }

        }

    def validate(self, attrs):
        print(attrs.get('password'))
        print(attrs.get('re_pwd'))
        return attrs