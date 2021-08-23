from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^task/$', views.TaskViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^task/update/(?P<pk>.*)/$', views.TaskViewSet.as_view({'post': 'update'})),
    url(r'^tasklist/$', views.TaskListViewSet.as_view({'get': 'list',})),

    # 任务状态
    url(r'^task_status/$', views.Task_StatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^task_status/update/(?P<pk>.*)/$', views.Task_StatusViewSet.as_view({'post': 'update'})),

    # 任务来源
    url(r'^task_priority/$', views.Task_PriorityViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^task_priority/update/(?P<pk>.*)/$', views.Task_PriorityViewSet.as_view({'post': 'update'})),

    # 任务附件
    url(r'^taskfile/$', views.TaskFileViewSet.as_view({'get': 'list', 'post': 'create'})),

    #
    url(r'^journal/$', views.JournalViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^journal/info/$', views.JournalViewSet.as_view({'get': 'retrieve'})),
    url(r'^journal/update/(?P<pk>.*)/$', views.JournalViewSet.as_view({'post': 'update'})),

    # 考勤汇总
    url(r'^summarizing/$', views.SummarizingViewSet.as_view({'get': 'list',})),

    #
    url(r'^car_rental/$', views.CarRentalViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^car_rental/update/(?P<pk>.*)/$', views.CarRentalViewSet.as_view({'post': 'update'})),

    #
    url(r'^work_status/$', views.StatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^work_status/update/(?P<pk>.*)/$', views.StatusViewSet.as_view({'post': 'update'})),

    # 工作环境
    url(r'^other_env/$', views.OtherEnvViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^other_env/update/(?P<pk>.*)/$', views.OtherEnvViewSet.as_view({'post': 'update'})),

    # 特殊环境
    url(r'^special_env/$', views.SpecialEnvViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^special_env/update/(?P<pk>.*)/$', views.SpecialEnvViewSet.as_view({'post': 'update'})),
]