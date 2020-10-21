from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^project/$', views.ProjectViewSet.as_view({'get': 'list'})),
    url(r'^project/create/$', views.ProjectCreateViewSet.as_view({'post': 'create'})),
    url(r'^project/updateInfo/(?P<pk>.*)/$', views.ProjectCreateViewSet.as_view({'get': 'retrieve', 'post': 'update'})),

    url(r'^project/manufacturer/$', views.ProjectManufacturerViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^project/monitortype/$', views.MonitorTypeViewSet.as_view({'get':'list',})),

    url(r'^detail/$', views.DetailViewSet.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^detail/(?P<pk>.*)/$', views.DetailViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    url(r'^server/$', views.ServerViewSet.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^facility/$', views.FacilityViewSet.as_view({'get':'list',})),
    url(r'^facility/(?P<pk>.*)/$', views.FacilityViewSet.as_view({'get':'retrieve'})),

    # 公司设备管理url
    url(r'^CoFaciliy/$', views.CollectorViewSet.as_view({'get': 'list'})),
    url(r'^CoFaciliy/create/$', views.CollectorViewSet.as_view({'post':'create'})),
    url(r'^CoFaciliy/aisle/$', views.AisleViewSet.as_view({'get':'list'})),
    url(r'^CoFaciliy/aisle/create/$', views.AisleViewSet.as_view({'post':'create'})),

    # 发货
]