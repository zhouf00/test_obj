# _*_ coding: utf-8 _*_
from rest_framework import serializers

from . import models


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class TaskFileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskFile
        fields = '__all__'


class JournalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkLogs
        fields = '__all__'
        # fields = ['id', ]


class SummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Summary
        fields = '__all__'


class StatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkStatus
        fields = '__all__'


class OtherEnvModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OtherEnv
        fields = '__all__'


class SpecialEnvModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpecialEnv
        fields = '__all__'


class CarRentalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarRental
        fields = '__all__'


class Task_StatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task_Status
        fields = '__all__'


class Task_PriorityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task_Priority
        fields = '__all__'