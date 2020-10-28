from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 项目信息
    url(r'^project/$', views.ProjectViewSet.as_view({'get': 'list'})),
    url(r'^project/create/$', views.ProjectCreateViewSet.as_view({'post': 'create'})),
    url(r'^project/updateInfo/(?P<pk>.*)/$', views.ProjectCreateViewSet.as_view({'get': 'retrieve', 'post': 'update'})),


    # 机房信息
    url(r'^idcroom/$', views.IdcRoomViewSet.as_view({'get': 'list'})),
    url(r'^idcroom/create/$', views.IdcRoomViewSet.as_view({'post': 'create'})),
    url(r'^idcroom/update/(?P<pk>.*)/$', views.IdcRoomViewSet.as_view({'post': 'update'})),

    # 发货
    url(r'^cargo/$', views.StockViewSet.as_view({'get': 'list'})),
    url(r'^cargo/create/$', views.StockViewSet.as_view({'post': 'create'})),
    url(r'^cargo/update/(?P<pk>.*)/$', views.StockViewSet.as_view({'post': 'update'})),
    url(r'^invoice/$', views.InvoiceViewSet.as_view({'get': 'list'})),
    url(r'^invoice/create/$', views.InvoiceViewSet.as_view({'post': 'create'})),
    url(r'^invoice/update/$', views.InvoiceViewSet.as_view({'post': 'update'})),

    # 标签
    url(r'^projectTag/manufacturer/$', views.ProjectManufacturerViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/manufacturer/update/(?P<pk>.*)/$', views.ProjectManufacturerViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/monitortype/$', views.MonitorTypeViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/monitortype/update/(?P<pk>.*)/$', views.MonitorTypeViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/type/$', views.ProjectTypeViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/type/update/(?P<pk>.*)/$', views.ProjectTypeViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/status/$', views.ProjectStatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/status/update/(?P<pk>.*)/$', views.ProjectStatusViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/area/$', views.ProjectAreaViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/area/update/(?P<pk>.*)/$', views.ProjectAreaViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/workingenv/$', views.ProjectWorkingEnvViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/workingenv/update/(?P<pk>.*)/$', views.ProjectWorkingEnvViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/StockFinish/$', views.StockViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/StockFinish/update/(?P<pk>.*)/$', views.StockViewSet.as_view({'post': 'update'})),

    # 图片上传
    url(r'^invoice/img/$', views.InvoiceImageViewSet.as_view({'get': 'list'})),
    url(r'^invoice/upload/$', views.InvoiceImageViewSet.as_view({'post': 'create'})),
]