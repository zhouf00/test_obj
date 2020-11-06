from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^menu/$', views.MenuViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^updatemenu/(?P<pk>.*)/$', views.MenuViewSet.as_view({'post': 'update'})),

    url(r'^role/$', views.AuthViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^updaterole/(?P<pk>.*)/$', views.AuthViewSet.as_view({'post': 'update'})),

    url(r'^role/change/(?P<pk>.*)/$', views.AuthChangeViewSet.as_view({'post': 'update'}))
]