from django.conf.urls import url, include

from . import views

urlpatterns = [
    # 公司产品管理url
    url(r'^$', views.ProductViewSet.as_view({'get': 'list'})),
    url(r'^create/$', views.ProductViewSet.as_view({'post':'create'})),
    url(r'^update/(?P<pk>.*)/$', views.ProductViewSet.as_view({'post': 'update'})),
    url(r'^list/$', views.ProductListViewSet.as_view({'get': 'list'})),

    #　生产出的产品
    url(r'^production/$', views.ProductionViewSet.as_view({'get': 'list'})),
    url(r'^production/create/$', views.ProductionViewSet.as_view({'post': 'create'})),
    url(r'^production/update/(?P<pk>.*)/$', views.ProductionViewSet.as_view({'post': 'update'})),

    # 标签
    url(r'^aisle/$', views.AisleViewSet.as_view({'get': 'list'})),
    url(r'^aisle/create/$', views.AisleViewSet.as_view({'post': 'create'})),
    url(r'^aisle/update/(?P<pk>.*)/$', views.AisleViewSet.as_view({'post': 'update'})),

    url(r'^status/$', views.PdStatusViewSet.as_view({'get': 'list','post': 'create'})),
    url(r'^status/update/$', views.PdStatusViewSet.as_view({'post': 'update'})),

    url(r'^lifecycle/$', views.LifecycleViewSet.as_view({'get': 'list'})),
    url(r'^lifecycle/create/$', views.LifecycleViewSet.as_view({'post': 'create'})),
    url(r'^lifecycle/update/(?P<pk>.*)/$', views.LifecycleViewSet.as_view({'post': 'update'})),

    url(r'^production_status/$', views.ProductionStatusViewSet.as_view({'get': 'list','post': 'create'})),
    url(r'^production_status/update/(?P<pk>.*)/$', views.ProductionStatusViewSet.as_view({'post': 'update'})),
]