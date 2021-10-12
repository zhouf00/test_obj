from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 项目信息
    url(r'^project/$', views.ProjectViewSet.as_view({'get': 'list'})),
    url(r'^project/create/$', views.ProjectViewSet.as_view({'post': 'create'})),
    url(r'^project/update/(?P<pk>.*)/$', views.ProjectViewSet.as_view({'post': 'update'})),
    url(r'^project/delete/(?P<pk>.*)/$', views.ProjectDeleteViewSet.as_view({'post': 'update'})),
    url(r'^project/classify/$', views.ProjectClassifyViewSet.as_view({'get': 'list'})),
    url(r'^project/list/$', views.ProjectListViewSet.as_view({'get': 'list'})),

    url(r'^project/overview/$', views.ProjectOverview.as_view()),
    # 收藏
    url(r'^project/collect/$', views.ProjectColletViewSet.as_view()),

    # 监测设备信息
    url(r'^facility/$', views.FacilityViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^facility/update/(?P<pk>.*)/$', views.FacilityViewSet.as_view({'post': 'update'})),

    # 时间轴
    url(r'^projectstatustime/$', views.ProjectStatusTimeViewSet.as_view({'get': 'list', 'post': 'my_post'})),

    # 项目更进
    url(r'^trace/$', views.ProjectTraceViewSet.as_view({'get': 'list', 'post':'create'})),

    # 外包商信息
    url(r'^contract/$', views.ContractViewSet.as_view({'get': 'list', 'post':'create'})),
    url(r'^contract/(?P<pk>.*)/$', views.ContractViewSet.as_view({'post': 'update'})),
    url(r'^outsourcer/$', views.OutsourcerViewSet.as_view({'get': 'list', 'post':'create'})),
    url(r'^outsourcer/list/$', views.OutsourcerListViewSet.as_view({'get': 'list'})),
    url(r'^outsourcer/(?P<pk>.*)/$', views.OutsourcerViewSet.as_view({'post': 'update'})),
    url(r'^payment/$', views.PaymentViewSet.as_view({'get': 'list', 'post':'create'})),
    url(r'^payment/(?P<pk>.*)/$', views.PaymentViewSet.as_view({'post': 'update'})),

    # 机房信息
    url(r'^idcroom/$', views.IdcRoomViewSet.as_view({'get': 'list'})),
    url(r'^idcroom/create/$', views.IdcRoomViewSet.as_view({'post': 'create'})),
    url(r'^idcroom/update/(?P<pk>.*)/$', views.IdcRoomViewSet.as_view({'post': 'update'})),

    # 发货
    url(r'^cargo/$', views.StockViewSet.as_view({'get': 'list'})),
    url(r'^cargo/create/$', views.StockViewSet.as_view({'post': 'create'})),
    url(r'^cargo/update/(?P<pk>.*)/$', views.StockViewSet.as_view({'post': 'update'})),
    url(r'^invoice/$', views.InvoiceViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^invoice/update/$', views.InvoiceViewSet.as_view({'post': 'update'})),
    url(r'^invoice/update_time/(?P<pk>.*)/$', views.InvoiceUpdateViewSet.as_view({'post': 'update'})),
    # 图片上传
    url(r'^invoice/img/$', views.InvoiceImageViewSet.as_view({'get': 'list'})),
    url(r'^invoice/upload/$', views.InvoiceImageViewSet.as_view({'post': 'create'})),

    # 标签
    url(r'^projectTag/manufacturer/$', views.ProjectManufacturerViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/manufacturer/update/(?P<pk>.*)/$', views.ProjectManufacturerViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/projectpriority/$', views.ProjectPriorityViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/projectpriority/update/(?P<pk>.*)/$', views.ProjectPriorityViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/projectpriority2/$', views.ProjectPriority2ViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/projectpriority2/update/(?P<pk>.*)/$', views.ProjectPriority2ViewSet.as_view({'post': 'update'})),

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
    url(r'^projectTag/StockFinish/(?P<pk>.*)/$', views.StockViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/monitornumber/$', views.MonitorNumberViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/monitornumber/update/(?P<pk>.*)/$', views.MonitorNumberViewSet.as_view({'post': 'update'})),

    url(r'^projectTag/tracestatus/$', views.TraceStatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^projectTag/tracestatus/update/(?P<pk>.*)/$', views.TraceStatusViewSet.as_view({'post': 'update'})),


]