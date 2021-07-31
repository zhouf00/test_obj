"""test_obj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings

import xadmin

urlpatterns = [
    url(r'^api/xadmin/', xadmin.site.urls),

    url(r'^api/back/', include('backend.urls')),
    url(r'^api/personnel/', include('personnel.urls')),
    url(r'^api/engineering/', include('engineering.urls')),
    url(r'^api/product/', include('product.urls')),
    url(r'^api/rbac/', include('rbac.urls')),
    url(r'^api/crm/', include('APPS.crm.urls')),
    url(r'^api/mlr/', include('APPS.mlr.urls')),


    url(r'^api/media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
