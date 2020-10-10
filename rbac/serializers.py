from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from . import models

class MenuModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Menu
        fields = ['id', 'title', 'url', 'parent', 'icon']


class RoleModelSerializer(serializers.ModelSerializer):

    permissions = MenuModelSerializer(many=True)

    class Meta:
        model = models.Role
        fields = ['id', 'title', 'permissions', 'count']