from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^market/$', views.MarketViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^market/update/(?P<pk>.*)/$', views.MarketViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
    url(r'^market/delete/(?P<pk>.*)/$', views.MarketDeleteViewSet.as_view({'post': 'update'})),

    url(r'^markettrace/$', views.MarketTraceViewSet.as_view({'get': 'list', 'post': 'create'})),

    url(r'^linkman/$', views.LinkmanViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^linkman/update/(?P<pk>.*)/$', views.LinkmanViewSet.as_view({'post': 'update'})),

    url(r'^raterecord/$', views.RateRecordViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^raterecord/update/(?P<pk>.*)/$', views.RateRecordViewSet.as_view({'post': 'update'})),

    url(r'history/$', views.MarketHistoryViewSet.as_view({'get':'list', 'post': 'create'})),
    url(r'history/update/(?P<pk>.*)/$', views.MarketHistoryViewSet.as_view({'put': 'update'})),
    url(r'history/annals/$', views.AnnalsViewSet.as_view()),
]