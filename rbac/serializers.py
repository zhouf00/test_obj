from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from . import models


class MenuModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Menu
        fields = ['id', 'title', 'url', 'parent', 'icon', 'name',
                  'parentInfo','childrenList']


class AuthModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Auth
        fields = ['id', 'title', 'memo', 'user', 'menu',
                  'menuList', 'userList',]
        extra_kwargs ={
            'user': {
                'read_only': True
            },
            'menu': {
                'read_only': True
            }
        }


class AuthChangeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Auth
        fields = ['id', 'user', 'menu']
        extra_kwargs = {
            'user': {
                'required': False
            },
            'menu': {
                'required': False
            },
        }
