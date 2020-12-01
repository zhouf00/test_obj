# _*_ coding: utf-8 _*_
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from personnel import models, serializers

from utils.response import APIResponse
from utils.my_request import MyRequest

from utils.authentications import JWTAuthentication
from utils.pagenations import MyPageNumberPagination


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 拿到前台登录信息，交给序列化类，规则：帐号用usr传，密码用pwd传
        user_obj =models.User.objects.filter(username=request.data['usr']).first()
        # print(user_obj)
        # print(type(request.data), request.data)
        user_ser = serializers.LoginModelSerializer(instance=user_obj, data=request.data)
        # 序列化类校验得到登录用户与token存放在序列化对象中
        user_ser.is_valid(raise_exception=True)
        user_ser.save()
        # 取出登录用户与token返回给前台
        return APIResponse(
            data_msg='post ok',
            token=user_ser.token,
            results=serializers.LoginModelSerializer(user_ser.user).data
        )


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        user_ser = serializers.LogoutModelSerializer(request.user, many=False)
        # user_ser = serializers.LoginModelSerializer(data=request.data)
        # user_ser.token = None
        user_ser.is_valid(raise_exception=True)
        return APIResponse(
            data_msg='logout'
        )


class auth2APIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # print(request.data)
        auth_requests = MyRequest()
        userId = auth_requests.get_user(request.data['code'])
        user_obj =models.User.objects.filter(username=userId['usr']).first()
        # print(user_obj)
        if user_obj:
            # print('用户存在')
            user_ser = serializers.AuthModelSerializer(instance=user_obj, data=userId)
            # 序列化类校验得到登录用户与token存放在序列化对象中
            user_ser.is_valid(raise_exception=True)
            user_ser.save()
        else:
            # print('用户不存在')
            userInfo = auth_requests.get_info(userId['usr'])
            # 默认为普通用户，数据库内 2 普通用户
            userInfo['auth'] = [2]
            user_create = serializers.AuthCreateUserModelSerializer(data=userInfo)
            user_create.is_valid(raise_exception=True)
            user_create.save()
            user_obj = models.User.objects.filter(username=userId['usr']).first()
            user_ser = serializers.AuthModelSerializer(instance=user_obj, data=userId)
            # 序列化类校验得到登录用户与token存放在序列化对象中
            user_ser.is_valid(raise_exception=True)
            user_ser.save()
        return APIResponse(
            data_status=userId['errcode'],
            data_msg=userId['errmsg'],
            token=user_ser.token,
            results=serializers.AuthModelSerializer(user_ser.user).data
        )


class UserViewSet(ModelViewSet):

    authentication_classes = [JWTAuthentication]

    def info(self, request, *args, **kwargs):
        # 拿到前台登录信息，交给序列化类，规则：帐号用usr传，密码用pwd传
        # 序列化类校验得到登录用户与token存放在序列化对象中
        # 取出登录用户与token返回给前

        user = serializers.UserModelSerializer(request.user, many=False).data

        return APIResponse(
            data_msg='get ok',
            results=user
        )


# 拉取所有用户信息
class UserInfoViewSet(ModelViewSet):

    queryset = models.User.objects.exclude(id=1).order_by('-last_login')
    serializer_class = serializers.UserModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields =['username', 'name']


class CreateUserViewSet(ModelViewSet):

    queryset = models.User.objects.exclude(id=1)
    serializer_class = serializers.CreateUserModelSerializer


class UpdateUserStatusViewSet(GenericViewSet, mixins.UpdateModelMixin):

    queryset = models.User.objects.exclude(id=1)
    serializer_class = serializers.UpdateStatusModelSerializer

    def my_update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return APIResponse(
            data_msg='post ok',
            results=request.data
        )


class UpdateUserDeptViewSet(ModelViewSet):

    queryset = models.User.objects.exclude(id=1)
    serializer_class = serializers.UpdateDeptModelSerializer


class UserListViewSet(ModelViewSet):

    queryset = models.User.objects.exclude(id=1)
    serializer_class = serializers.UserListModelSerializer


class DeptViewSet(ModelViewSet):

    queryset = models.Structure.objects.all().order_by('parentid')
    serializer_class = serializers.DeptModelSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields =['parentid']


class DeptListViewSet(ModelViewSet):

    queryset = models.Structure.objects.filter(parentid=1)
    serializer_class = serializers.DeptListModelSerializer

