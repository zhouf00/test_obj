# _*_ coding: utf-8 _*_
import datetime
from rest_framework import serializers, exceptions
from rest_framework_jwt.settings import api_settings

from personnel import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# 用户密码登陆
class LoginModelSerializer(serializers.ModelSerializer):

    # 自定义序列化属性
    usr = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = [
            # 数据库字段
            'username', 'usr', 'pwd', 'mobile',
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
        # print('内部打印', attrs)
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
        raise serializers.ValidationError({'msg': '账号或密码错误'})


# 企业微信登陆
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
        # print('内部打印', attrs)
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
        raise serializers.ValidationError({'msg': '账号可能未启用'})


class AuthCreateUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['username', 'mobile', 'name', 'is_active', 'position',
                  'avatar', 'gender', 'auth','department']

    def validate(self, attrs):
        attrs['is_active'] = True
        return attrs


class LogoutModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User

    def validate(self, attrs):
        self.token = None
        return attrs


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'username', 'mobile', 'name', 'last_login', 'gender', 'avatar',
                  'is_active', 'email', 'position', 'auth',
                  'menus','markethistoryInfo', 'project'
                  ]


class CreateUserModelSerializer(serializers.ModelSerializer):

    pwd = serializers.CharField(
        required=False,
        min_length=6,
        error_messages={
            'min_length': '密码最少6位'
        })
    re_pwd = serializers.CharField(
        required=False,
        min_length=6,
        error_messages={
            'min_length': '密码最少6位'
        })

    class Meta:
        model = models.User
        fields = ['username', 'mobile', 'name', 'password', 'pwd', 're_pwd', 'is_active']
        extra_kwargs ={
            'password': {
                'required': False
            },
            'pwd': {
                'required': False
            },
            're_pwd': {
                'required': False
            },
        }

    def validate(self, attrs):
        if 'pwd' in attrs:
            pwd = attrs.pop('pwd')
            re_pwd = attrs.pop('re_pwd') if 're_pwd' in attrs else ''   # 取出校验
            if not pwd:
                raise exceptions.ValidationError({'pwd': '密码不能为空'})
            if pwd != re_pwd:
                raise exceptions.ValidationError({'pwd': '两次密码不一致'})
            else:
                attrs['password'] = pwd
        return attrs


    def create(self, validated_data):
        user = super().create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user


class UpdateStatusModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'is_active']
        extra_kwargs = {
            'is_active': {
                'write_only': True
            }
        }


class UpdateDeptModelSerializer(serializers.Serializer):

    class Meta:
        model = models.User
        fields = ['id', 'department']

    def validate(self, attrs):
        # attrs['users'] = attrs.pop('member')
        # print('修改', self.instance, attrs)
        return attrs

    def update(self, instance, validated_data):
        instance.departments.set(validated_data.get('department', instance.departments))

        return instance


class UpdateUserProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'project']


class UserListModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id','username', 'name', 'project', 'department', 'position', 'avatar']


class DeptModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Structure
        fields = ['id', 'deptid', 'name', 'parentid', 'order',
                  'childrenList', 'leaders', 'leaderList', 'usersInfoList', 'userList']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class DeptListModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Structure
        fields = ['id','deptid', 'name', 'childrenList']


class DeptUserUpdateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Structure
        fields = ['id', 'users', 'type', 'test']

    def validate(self, attrs):

        # print('修改', self.instance, attrs)
        return attrs


class DeptToUserSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class DeptToUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeptToUser
        fields = ['id', 'user', 'department', 'isleader']
        list_serializer_class = DeptToUserSerializer