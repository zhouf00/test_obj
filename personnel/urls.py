from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [

    url(r'^login/$', views.LoginAPIView.as_view()),
    url(r'^logout/$', views.LogoutAPIView.as_view()),
    url(r'^auth2/$', views.auth2APIView.as_view()),
    url(r'^user/$', views.UserViewSet.as_view({'get':'info'})),

    url(r'^list/$', views.UserinfoViewSet.as_view({'get':'list'})),
    url(r'^register/$', views.CreateUserViewSet.as_view({'post': 'create'})),
    url(r'^updateuser/(?P<pk>.*)/$', views.UpdateUserViewSet.as_view({'post': 'update'})),
    url(r'^updatestatus/(?P<pk>.*)/$', views.UpdateStatusViewSet.as_view({'post': 'my_update'})),
    url(r'^userlist/$', views.UserListViewSet.as_view({'get':'list'}))

    # url(r'^structure/$', views.DeptViewSet.as_view({'get':'list', 'pa'})),
    # url(r'^structure/$', views.DeptViewSet.as_view({'get':'list', 'post': 'create'})),
    # url(r'^structure/(?P<pk>.*)/$', views.DeptViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'}))
]