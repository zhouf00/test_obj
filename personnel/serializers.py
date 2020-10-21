import re
import datetime
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from personnel import models
from rbac.serializers import RoleModelSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginModelSerializer(serializers.ModelSerializer):

    # 自定义序列化属性
    usr = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = [
            # 数据库字段
            'username', 'usr', 'pwd', 'mobile', #'last_login'
        ]
        extra_kwargs = {
            'username':{
                'read_only': True
            },
            'mobile': {
                'read_only': True
            },
        }

    def validate(self, attrs):
        print('内部打印', attrs)
        usr = attrs.pop('usr')
        pwd = attrs.pop('pwd')
        user_query = models.User.objects.filter(username=usr)
        user_obj = user_query.first()
        if user_obj and user_obj.check_password(pwd):
            # 签发token，将token存放到，实例化类对象中
            payload = jwt_payload_handler(user_obj)
            self.token = jwt_encode_handler(payload)
            # 将当前用户与签发的token都保存在序列化对象中
            self.user = user_obj
            # 写入最后登陆时间
            attrs['last_login'] = datetime.datetime.today()
            return attrs
        raise serializers.ValidationError({'msg': '数据有误'})


class AuthModelSerializer(serializers.ModelSerializer):

    usr = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['username', 'usr', 'avatar']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'roles': {
                'required': False
            }
        }

    def validate(self, attrs):
        print('内部打印', attrs)
        usr = attrs.pop('usr')
        user_query = models.User.objects.filter(username=usr)
        user_obj = user_query.first()
        if user_obj:
            # 签发token，将token存放到，实例化类对象中
            payload = jwt_payload_handler(user_obj)
            self.token = jwt_encode_handler(payload)
            # 将当前用户与签发的token都保存在序列化对象中
            self.user = user_obj
            # 写入最后登陆时间
            attrs['last_login'] = datetime.datetime.today()
            # 默认给普通用户权限
            return attrs
        raise serializers.ValidationError({'errmsg': '数据有误或帐号不存在'})


class AuthCreateUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['username', 'mobile', 'name', 'is_active', 'roles',
                  'avatar', 'gender']

    def validate(self, attrs):
        attrs['is_active'] = True
        attrs['roles'] = [2]
        return attrs


class LogoutModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User

    def validate(self, attrs):
        self.token = None
        return attrs


class UserModelSerializer(serializers.ModelSerializer):

    roles = RoleModelSerializer(many=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        if obj.is_active:
            return 1
        else:
            return 0

    class Meta:
        model = models.User
        fields = ['id', 'username', 'mobile', 'name', 'last_login', 'status', 'gender', 'roles', 'avatar',
                  'is_active', 'password', 'email']
        extra_kwargs = {
            'is_active': {
                'write_only': True
            }
        }


class CreateUserModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ['username', 'mobile', 'name', 'password', 'is_active']


class UpdateUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'username', 'mobile', 'name', 'password', 'is_active']


class UpdateStatusModelSerializer(serializers.ModelSerializer):

    status = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'status', 'is_active']
        extra_kwargs = {
            'is_active': {
                'write_only': True
            }
        }


class UserListModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'name', 'project']


class DeptListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class DeptModelSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Structure
        list_serializer_class = DeptListSerializer
        fields = ['id',
                  'deptid', 'name', 'parentid', 'order']
        extra_kwargs = {
            'deptid':{
                'required': False
            },
            'parentid': {
                'required': False
            },
        }

    def validate(self, attrs):
        # print(attrs)
        if models.Structure.objects.filter(deptid=attrs['id']):
            raise serializers.ValidationError({'data': '部门已存在'})
        attrs['deptid'] = attrs.pop('id')
        print(attrs)
        return attrs

