from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^project/$', views.ProjectViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^detail/$', views.DetailViewSet.as_view({'get': 'list'})),
    # url(r'^detail/(?P<pk>.*)/$', views.DetailViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    url(r'^server/$', views.ServerViewSet.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^facility/$', views.FacilityViewSet.as_view({'get':'list',})),
    url(r'^facility/(?P<pk>.*)/$', views.FacilityViewSet.as_view({'get':'retrieve'}))
]