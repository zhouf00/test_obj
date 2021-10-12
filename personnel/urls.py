from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [

    url(r'^login/$', views.LoginAPIView.as_view()),
    url(r'^logout/$', views.LogoutAPIView.as_view()),
    url(r'^auth2/$', views.auth2APIView.as_view()),
    url(r'^userinfo/$', views.UserViewSet.as_view({'get':'info'})),

    url(r'^list/$', views.UserInfoViewSet.as_view({'get':'list'})),
    url(r'^userlist/$', views.UserListViewSet.as_view({'get': 'list'})),
    url(r'^register/$', views.CreateUserViewSet.as_view({'post': 'create'})),
    url(r'^updateuser/(?P<pk>.*)/$', views.CreateUserViewSet.as_view({'post': 'update'})),
    url(r'^updateuserstatus/(?P<pk>.*)/$', views.UpdateUserStatusViewSet.as_view({'post': 'my_update'})),
    url(r'^updateuserproject/(?P<pk>.*)/$', views.UpdateUserProjectViewSet.as_view({'post': 'update'})),
    url(r'userleaders/$', views.UserLeaderViewSet.as_view()),

    url(r'^structure/$', views.DeptViewSet.as_view({'get': 'list'})),
    url(r'^structure/create/$', views.DeptViewSet.as_view({'post': 'create'})),
    url(r'^structure/update/(?P<pk>.*)/$', views.DeptViewSet.as_view({'post': 'update'})),
    url(r'^structure/list/$', views.DeptListViewSet.as_view({'get': 'list'})),

    url(r'dept_user/$', views.DeptToUserViewSet.as_view()),
    url(r'dept_leader/$', views.DeptLeaderViewSet.as_view()),
    url(r'overview_area/$', views.OverviewAreaViewSet.as_view()),
]