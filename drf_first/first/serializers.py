from rest_framework import serializers, exceptions

from first.models import Teacher, Department


#序列化器
class TeacherSerializer(serializers.Serializer):
    name = serializers.CharField()
    gender = serializers.SerializerMethodField()
    # department = serializers.CharField()
    age = serializers.IntegerField()

    def get_gender(self, obj):
        return obj.get_gender_display()

#反序列化器
class TeacherDeSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=20,
        min_length=2,
        error_messages={
            'max_length': '长度太长了',
            'min_length': '长度太短了',
        }
    )
    gender = serializers.IntegerField()
    age = serializers.IntegerField()
    # department = serializers.CharField(max_length=20)

    #全局钩子函数
    def validate(self, attrs):
        if attrs.get('age') < 0:
            raise exceptions.ValidationError('年龄填写错误！')
        return attrs

    #局部钩子函数
    def validate_gender(self, obj):
        l = [0, 1, 2]
        if obj not in l:
            raise exceptions.ValidationError('性别填写错误')
        return obj


    def create(self, validated_data):
        return Teacher.objects.create(**validated_data)

#ModelSerializer
class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name', 'age', 'department', 'gender1')
        # fields = "__all__"
        #
        depth = 1


class DepartmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department

