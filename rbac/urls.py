from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^menu/', views.MenuViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^role/', views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})),

]