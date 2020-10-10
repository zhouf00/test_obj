from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^jsapi/$', views.JsApiAPIView.as_view()),
]