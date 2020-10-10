from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins
from rest_framework.response import Response

from rbac import models, serializers

from utils.authentications import JWTAuthentication

# Create your views here.

class MenuViewSet(ModelViewSet):

    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuModelSerializer


class RoleViewSet(ModelViewSet):

    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleModelSerializer

