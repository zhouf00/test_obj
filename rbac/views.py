from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rbac import models, serializers, filters

from utils.authentications import JWTAuthentication

# Create your views here.

class MenuViewSet(ModelViewSet):

    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuModelSerializer

    filter_class = filters.MenuFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]


class AuthViewSet(ModelViewSet):

    queryset = models.Auth.objects.all()
    serializer_class = serializers.AuthModelSerializer

    filter_class = filters.AuthFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]


class AuthChangeViewSet(ModelViewSet):

    queryset = models.Auth.objects.all()
    serializer_class = serializers.AuthChangeModelSerializer