import re
from rest_framework import serializers

from django.contrib.auth.models import Group
from personnel import models


class UserModelSerializer(serializers.ModelSerializer):

    # 自定义序列化属性
    # isleader_in_dept = serializers.


    userid = serializers.CharField(write_only=True) # 企业微信ID
    # department = serializers.ListField(write_only=True) # 企业微信部门
    is_leader_in_dept = serializers.ListField(write_only=True) # 企业微信是否为部门领导

    class Meta:
        model = models.User
        fields = [
            # 前台输入字段
            'userid', 'is_leader_in_dept',
            # 数据库字段
            'username', 'name', 'mobile', 'gender', 'email', 'avatar', 'is_active', 'leader_dept',
            'main_department', 'department'
        ]
        extra_kwargs = {
            'username':{
                'read_only': True
            },
            'leader_dept': {
                'read_only': True
            },
        }

    def validate(self, attrs):
        attrs['username'] = attrs.pop('userid')
        attrs['depts'] = attrs.pop('department')
        attrs['leader_dept'] = []
        if len(attrs['depts']) != len(attrs['is_leader_in_dept']):
            raise serializers.ValidationError({'data': '部门有误'})
        for i in range(len(attrs['depts'])):
            if attrs['is_leader_in_dept'][i]:
                attrs['leader_dept'].append(attrs['depts'][i])
        attrs.pop('is_leader_in_dept')
        return attrs


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

