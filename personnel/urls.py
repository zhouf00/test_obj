from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^user/$', views.UserViewSet.as_view({'get':'list', 'post': 'create'})),

    # url(r'^structure/$', views.DeptViewSet.as_view({'get':'list', 'pa'})),
    url(r'^structure/$', views.DeptViewSet.as_view({'get':'list', 'post': 'create'})),
    url(r'^structure/(?P<pk>.*)/$', views.DeptViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'}))
]