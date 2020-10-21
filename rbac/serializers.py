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
        fields = ['id', 'title','memo','leader_list', 'leader','status', 'user_list']
        extra_kwargs = {
            'leader': {
                'write_only': True,
                'required': False
            },
            'leader_list': {
                'read_only': True,
            },
            'user_list': {
                'read_only':True
            },
        }

    def validate(self, attrs):
        return attrs