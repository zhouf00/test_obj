from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from . import models


class MenuModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Menu
        fields = ['id', 'title', 'url', 'parent', 'icon']


class RoleModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Role
        fields = ['id', 'title','memo','leaders_list','status', 'user_list', 'leaders']

class AuthModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Auth
        fields = ['id', 'user', 'userName', 'role', 'memo', 'menu']