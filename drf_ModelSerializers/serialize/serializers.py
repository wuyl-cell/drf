from rest_framework import serializers

from serialize.models import Teacher, Department


class DepartmentModelsSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('de_name', 'people_num')


class TeacherModelsSerializers(serializers.ModelSerializer):
    # department = DepartmentModelsSerialisers()
    def validate(self, attrs):
        return attrs

    def validate_gender(self, obj):
        print(obj)
        return obj
    class Meta:
        model = Teacher
        fields = ('name', 'gender', 'department')
        extra_kwargs = {
            'name': {
                'required': True,
                'max_length': 10,
                "min_length": 2,
                'error_messages': {
                    'required': '名称是必填字段',
                    'min_length': '名称不能少于两个字符'
                }
            },

        }


        # fields = '__all__'
        # depth = 1