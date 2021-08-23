import datetime
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count

from mlr import models, serializers, filters
from personnel import models as p_models
from engineering import models as e_models
from engineering import serializers as e_serializers
from product import models as product_models
from product import serializers as product_serializers
from utils.response import APIResponse
from utils.pagenations import MyPageNumberPagination
from utils.Push_message import  test_messages


class TaskViewSet(ModelViewSet):
    queryset = models.Task.objects.all().order_by('-create_time')
    serializer_class = serializers.TaskModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.TaskFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def get_queryset(self):
        super().get_queryset()
        # 拿到管理员身份
        role = self.request.user.roleList
        if '超级管理员' in role:
            self.isleader = True
            # print('你是管理员')
            pass
        else:
            # 拿到部门领导身份
            if self.request.user.deptList:
                # print('你是部门领导')
                self.isleader = True
                self.queryset = self.queryset.filter(Q(submitter__in=self.request.user.deptmembers[2]) |
                                                     Q(executor__in=self.request.user.deptmembers[2]) |
                                                     Q(subscriber__in=self.request.user.deptmembers[2])).distinct()
            else:
                # print('你不是部门领导')
                self.isleader = False
                self.queryset = self.queryset.filter(
                    Q(executor=self.request.user.id) | Q(submitter=self.request.user.id) | Q(subscriber=self.request.user.id)
                ).distinct()
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        # 关联信息
        userlist = p_models.User.objects.all()
        projectlist = e_models.Project.objects.all()
        # status = [{'id':1,'title': '未完成'}, {'id':2,'title': '已完成'},]
        status = models.Task_Status.objects.values('id', 'title')

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.addInfo(serializer.data, userlist, projectlist, status)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.addInfo(serializer.data, userlist, projectlist, status)
        return APIResponse(
            data_msg='post ok',
            results=serializer.data)

    def addInfo(self, data, userlist, projectlist, status):
        for var in data:
            user_list = userlist.filter(id__in=var['executor']+var['subscriber']+[var['submitter']]).values('id', 'name')
            for v in user_list:
                if v['id'] in var['executor']:
                    var['executorInfo'] = v
                    break
                else:
                    var['executorInfo'] = {}
            for v in user_list:
                if var['submitter'] == v['id']:
                    var['submitterInfo'] = v
                    break
                else:
                    var['submitterInfo'] = {}
            var['subscriberList'] = [v for v in user_list if v['id'] in var['subscriber']]
            var['projectInfo'] =  projectlist.filter(id=var['project']).values('id', 'name').first() if var['project']  else {}
            var['statusInfo'] = [v for v in status if v['id'] == var['status'] ][0]


class TaskListViewSet(ModelViewSet):

    queryset = models.Task.objects.all().order_by('-create_time')
    serializer_class = serializers.TaskModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.TaskFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]


class TaskFileViewSet(ModelViewSet):
    queryset = models.TaskFile.objects.all()
    serializer_class = serializers.TaskFileModelSerializer

    filter_class = filters.TaskfileFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['title'] = data['file'].name
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return APIResponse(results=serializer.data)


class JournalViewSet(ModelViewSet):
    queryset = models.WorkLogs.objects.all().order_by('-create_time')
    serializer_class = serializers.JournalModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.JournalFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

    isleader = False

    def get_queryset(self):
        super().get_queryset()
        # 拿到管理员身份
        role = self.request.user.roleList
        if '超级管理员' in role:
            self.isleader = True
            # print('你是管理员')
            pass
        else:
            # 拿到部门领导身份
            if self.request.user.deptList:
                # print('你是部门领导')
                self.isleader = True
                self.queryset = self.queryset.filter(Q(user__in=self.request.user.deptmembers[2])).distinct()
            else:
                # print('你不是部门领导')
                self.isleader = False
                self.queryset = self.queryset.filter(
                    Q(user=self.request.user.id)).distinct()
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        if 'project' in request.query_params and request.query_params['project']:
            project_id = request.query_params['project']
        else:
            project_id = None
        date = datetime.datetime.now()
        instance = self.queryset.filter(create_time__year=date.strftime('%Y'),
                                        create_time__month=date.strftime('%m'),
                                        create_time__day=date.strftime('%d'),
                                        user=self.request.user.id)

        # 关联信息
        project = e_models.Project.objects.filter(is_delete=False)
        projectLog_obj = e_models.ProjectTrace.objects.filter(is_delete=False)
        productionLog_obj = product_models.ProductionLog.objects.filter(is_delete=False)
        if instance:

            serializer = self.get_serializer(instance,many=True)
            res = serializer.data[0]
            res['project'] = project_id
            self.add_summary(res, projectLog_obj, productionLog_obj=productionLog_obj, project=project)
            if 'workList' not in res:
                res['workList'] = [{'facilityList':[{}]}]
        else:
            res = {
                'project': project_id,
                'content':'',
                'finish_time':'',
                'workList': [{
                    'facilityList': [{}]}]
            }
            self.add_summary(res, projectLog_obj, project=project, productionLog_obj=productionLog_obj)

        return APIResponse(
            results=res
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        # 关联信息
        project = e_models.Project.objects.filter(is_delete=False)
        projectTrace_list = e_models.ProjectTrace.objects.filter(is_delete=False)
        user_list = p_models.User.objects.exclude(id=1)
        status = models.WorkStatus.objects.all()
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.add_summary(serializer.data, projectTrace_list, status, project, user_list=user_list)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.add_summary(serializer.data, projectTrace_list, status, project, user_list=user_list)
        return APIResponse(
            data_msg='list ok',
            results=serializer.data)

    def create(self, request, *args, **kwargs):
        date = datetime.datetime.now()
        if 'workList' in request.data and not request.data['workList'][0]:
            # 未解决抛出异常，用API用代替
            return APIResponse(
                data_status='400',
                data_msg='',
                err='工作未填写'
            )

        instance = self.queryset.filter(
            create_time__year=date.strftime('%Y'),
            create_time__month=date.strftime('%m'),
            create_time__day=date.strftime('%d'),
            user=self.request.user.id
        ).first()
        if instance:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        e = self.to_projectLog(request.data, serializer.data['id'])
        if e:
            return APIResponse(
                data_status='400',
                data_msg='',
                err='工作内容有误, %s'%e
            )
        else:
            self.pLog_save(request.data)
            self.to_content(serializer.data, request.data)
        return APIResponse(
            data_msg='create ok',
            results=serializer.data,
        )

    def update(self, request, *args, **kwargs):
        if 'workList' in request.data and not request.data['workList']:
            # 未解决抛出异常，用API用代替
            return APIResponse(
                data_status='400',
                data_msg='',
                err='工作未填写'
            )

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        e = self.to_projectLog(request.data, serializer.data['id'])
        if e:
            return APIResponse(
                data_status='400',
                data_msg='',
                err='工作内容有误,%s' % e
            )
        else:
            self.pLog_save(request.data)
            self.to_content(serializer.data, request.data)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return APIResponse(data_msg='update ok',
            results=serializer.data,)

    def to_content(self, ser, data, *args, **kwargs):
        if 'content' in data:
            partial = kwargs.pop('partial', False)
            instance = self.queryset.filter(id=ser['id']).first()
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

    # 项目跟进
    def to_projectLog(self, data, worklog):
        user = self.request.user.id
        date = datetime.datetime.now()

        # 关联信息
        # project = e_models.Project.objects.filter(is_delete=False)  # 项目
        facility_obj = e_models.Facility.objects.filter(is_delete=False)    # 设备
        production_obj = product_models.Production.objects.filter(is_delete=False)
        productionLog_obj = product_models.ProductionLog.objects.filter(
                create_time__year=date.strftime('%Y'),
                create_time__month=date.strftime('%m'),
                create_time__day=date.strftime('%d'),)
        try:
            # 遍历工作
            for var in data['workList']:
                # 判断是否有项目
                # print('打印', var)
                if 'project_id' in var and var['project_id']:
                    var['project'] = var['project_id']
                    # 判断项目是否与定位相同
                    if 'project' in data and var['project'] == data['project']:
                        if 'user_id' in var and var['user_id'] != user:
                            var['user'] = var['user_id']
                            var['subscriber'].append(user)
                            v_worklog = var['worklog']
                            if 'ln_worklog' not in data :
                                data['ln_worklog'] = v_worklog
                            elif 'ln_worklog' in data and not data['ln_worklog']:
                                data['ln_worklog'] = v_worklog
                        else:
                            var['user'] = user
                            var['worklog'] = worklog
                            v_worklog = worklog
                            if 'subscriber' not in var:
                                var['subscriber'] = []
                    else:
                        #
                        if 'user_id'not in var:
                            var['user'] = user
                        else:
                            var['user'] = var['user_id']
                        var['worklog'] = worklog
                        v_worklog = worklog
                        if 'subscriber' not in var:
                            var['subscriber'] = []
                else:
                    if 'id' in var and var['id'] and not var['project_id']:
                        var.clear()
                        continue
                    data['content'] = var['facilityList'][0]['content']
                    continue
                new_log = []
                tmp_head = ''
                tmp_content = ''
                if 'content' not in var:
                    var['content'] = ''
                else:
                    var['content'] = var['content'].split('\t')[0]
                for v in var['facilityList']:
                    v['project'] = var['project']
                    if not var['project']:
                        tmp_content += ','.join(v['content'].strip())
                    v['user'] = var['user']
                    v['subscriber'] = var['subscriber']
                    v['worklog'] = var['worklog']
                    facility = v['facility'] if 'facility' in v else None
                    production = v['production'] if 'production' in v else None
                    if facility or production:
                        # print('有风机', v_worklog)
                        self.to_productionLog(v, productionLog_obj.filter(worklog=v_worklog, project=v['project']), new_log)
                        tmp_content += '\t设备：{facility}\n采集器：{production}\n描述：{content}\n'.format(
                            facility=facility_obj.filter(id=facility).first(),
                            production=production_obj.filter(id=production).first(),
                            content=v['content'])
                    else:
                        # print('没风机', v)
                        tmp_head = v['content'].strip()
                self.del_productionLog(productionLog_obj.filter(worklog=v_worklog, project=var['project']), new_log)
                var['content'] = tmp_head+'\n'+tmp_content
        except Exception as e:
            # print(e)
            return e

    # 项目跟进保存
    def pLog_save(self, data):
        date = datetime.datetime.now()
        project_obj = e_models.Project.objects.all()
        user_obj = p_models.User.objects.exclude(is_active=False)
        pLog_obj = e_models.ProjectTrace.objects.filter(
                create_time__year=date.strftime('%Y'),
                create_time__month=date.strftime('%m'),
                create_time__day=date.strftime('%d'),
        )
        new = []
        for var in data['workList']:
            if 'id' in var:
                pLog_ser = e_serializers.ProjectTraceModelSerializer(instance=pLog_obj.filter(id=var['id']).first(), data=var)
            else:
                if 'content' not in var:
                    continue
                pLog_ser = e_serializers.ProjectTraceModelSerializer(data=var)
            if pLog_ser.is_valid():
                pLog_ser.save()
                if 'user' in pLog_ser.data and pLog_ser.data['user'] == self.request.user.id:
                    if 'submitted' in data and data['submitted']:
                        test_messages(pLog_ser.data, project_obj, user_obj, self.request.user)
                    else:
                        print(data['submitted'])
                new.append(pLog_ser.data['id'])
            else:
                return APIResponse(
                    data_status='400',
                    data_msg='',
                    # err='产品日志更新错误'
                    err='[项目]%s'%pLog_ser.errors,
                )
        pLog_obj.filter(user=data['user']).exclude(id__in=new).delete()
        del_obj = pLog_obj.filter(subscriber=data['user']).exclude(id__in=new)
        if del_obj:
            # print('项目删除',del_obj.first().id)
            data['ln_worklog'] = None
            e_models.ProjectTrace.objects.get(id=del_obj.first().id).subscriber.remove(data['user'])

    # 产品跟进保存
    def to_productionLog(self, v, obj, new=None):
        # print('产品',obj)
        if 'id' in v:
            ser = product_serializers.ProductionLogModelSerializer(instance=obj.filter(id=v['id']).first(), data=v)
        else:
            ser = product_serializers.ProductionLogModelSerializer(data=v)
        if ser.is_valid():
            ser.save()
            new.append(ser.data['id'])
        else:
            return APIResponse(
                data_status='400',
                data_msg='',
                # err='产品日志更新错误'
                err='[产品]%s'%ser.errors,
            )

    # 产品删除
    def del_productionLog(self, obj, old):
        # print('删除', old, obj.exclude(id__in=old))
        obj.exclude(id__in=old).delete()

    # 获取数据时，添加内容
    def add_summary(self, data, projectTrace_list, status=None, project=None, productionLog_obj=None, user_list=None):
        date = datetime.datetime.now()
        if isinstance(data, list):
            for var in data:
                worklog_list = []
                worklog_list.append(var['id'])
                if 'ln_worklog' in var and var['ln_worklog']:
                    worklog_list.append(var['ln_worklog'])
                var['work_statusInfo'] = status.filter(id=var['work_status']).values().first()
                user = user_list.filter(id=var['user']).values('id', 'name').first()
                var['userInfo'] = user if user else {}
                content = projectTrace_list.filter(worklog__in=worklog_list).filter(
                    Q(user=var['user'])|Q(subscriber=var['user'])).values('project','content')
                content = ''.join(['<%s>\n\t %s'%(project.filter(id=v['project']).first(),v['content']) for v in content ])
                var['content'] = '%s %s'%(var['content'], content) if var['content'] else content
        else:
            if 'id' in data:
                if 'ln_worklog' in data and data['ln_worklog']:
                    worklog = [data['id'], data['ln_worklog']]
                else:
                    worklog = [data['id']]
                pt_obj = projectTrace_list.filter(worklog__in=worklog).values()
                project_list = [v['project_id'] for v in pt_obj if v['project_id']]
                workList = list(pt_obj)
                workList += list(projectTrace_list.filter(
                    create_time__year=date.strftime('%Y'),
                    create_time__month=date.strftime('%m'),
                    create_time__day=date.strftime('%d'),
                    project=data['project'],
                    worklog__isnull=False)
                    .exclude(project__in=project_list).values())
                if workList:
                    for var in workList:
                        var['subscriber'] = [v['subscriber'] for v in
                                                projectTrace_list.filter(worklog=var['worklog'], project=var['project_id']).values('subscriber')
                                                if v['subscriber']]
                # print(workList)
            else:
                if data['project']:
                    # print('无日志，有项目')
                    builders = [v['builders'] for v in project.filter(id=data['project']).values('builders')]
                    obj = projectTrace_list.filter(
                    create_time__year=date.strftime('%Y'),
                    create_time__month=date.strftime('%m'),
                    create_time__day=date.strftime('%d'), project=data['project']).filter(
                        Q(user__in=builders) | Q(subscriber=self.request.user.id))
                    workList = list(obj.values())
                    if workList:
                        workList[0]['subscriber'] = [v['subscriber'] for v in
                                                 obj.values('subscriber')
                                                 if v['subscriber']]
                else:
                    return
            for var in workList:
                headline = var['content'].split('\t')
                worklog = var['worklog']
                content = productionLog_obj.filter(worklog=worklog, project=var['project_id']).values()
                if not content and len(headline) > 0:
                    # print('不存在')
                    var['facilityList'] = [{
                        'content': headline[0]
                    }]
                elif len(content) < len(headline):
                    # print('存在')
                    var['facilityList'] = [{
                        'content': headline[0]
                    }]
                    var['facilityList'] += content
                else:
                    var['facilityList'] = content
            if data['content']:
                data['workList'] = [{'facilityList': [{'content': data['content']}]}] + workList
            else:
                data['workList'] = workList
            if not data['workList'] and not workList:
                data['workList'] = [{'facilityList': [{'content': data['content']}]}]


class SummarizingViewSet(ModelViewSet):

    queryset = models.WorkLogs.objects.all().order_by('user')
    serializer_class = serializers.JournalModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        # 关联信息
        user_list = p_models.User.objects.exclude(id=1).exclude(is_active=False)
        users = self.get_users(user_list)

        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(queryset, many=True)

        return APIResponse(
            data_msg='post ok',
            results=self.to_month(users, queryset))

    def to_month(self, users, data, time=None):
        t = datetime.datetime.now()
        year = t.strftime('%Y')
        month = t.strftime('%m')
        days = (datetime.date(t.year,t.month+1,1)-datetime.timedelta(1)).day
        nano_dict = {v['id']:v['title'][0:1] for v in models.WorkStatus.objects.values('id','title')}
        res_list = []
        default_tmp = {}
        for i in range(1, days + 1):
            default_tmp['%d日'%i] = ''
        for user in users:
            tmp = {
                'name': user['name']
            }
            tmp.update(default_tmp)
            td = data.filter(
                update_time__year= year,
                update_time__month=month,
                user=user['id']).order_by('-update_time').values('update_time__day','work_status')
            for var in td:
                print('%d日'%var['update_time__day'], var['work_status'])
                tmp['%d日'%var['update_time__day']] = [ var['work_status'], nano_dict[var['work_status']] ]
            res_list.append(tmp)
        return res_list

    def get_users(self, users):
        # 拿到管理员身份
        role = self.request.user.roleList
        if '超级管理员' in role:
            # print('你是管理员')
            pass
        elif '普通用户'in role and len(role)>1:
            pass
        else:
            # 拿到部门领导身份
            if self.request.user.deptList:
                users = users.filter(name__in=self.request.user.deptmembers[1]).distinct()
            else:
                users = users.filter(Q(name=self.request.user.name) |
                                     Q(id=self.request.user.id)).distinct()
        return users.values('id', 'name')


# 不用
class SummaryViewSet(ModelViewSet):
    queryset = models.Summary.objects.all()
    serializer_class = serializers.SummaryModelSerializer


#############
#
#############
class StatusViewSet(ModelViewSet):
    queryset = models.WorkStatus.objects.all().order_by('sort')
    serializer_class = serializers.StatusModelSerializer


class OtherEnvViewSet(ModelViewSet):
    queryset = models.OtherEnv.objects.all().order_by('sort')
    serializer_class = serializers.OtherEnvModelSerializer


class SpecialEnvViewSet(ModelViewSet):
    queryset = models.SpecialEnv.objects.all().order_by('sort')
    serializer_class = serializers.SpecialEnvModelSerializer


class CarRentalViewSet(ModelViewSet):
    queryset = models.CarRental.objects.all().order_by('sort')
    serializer_class = serializers.CarRentalModelSerializer


# 任务状态
class Task_StatusViewSet(ModelViewSet):
    queryset = models.Task_Status.objects.all().order_by('sort')
    serializer_class = serializers.Task_StatusModelSerializer

# 来源
class Task_PriorityViewSet(ModelViewSet):
    queryset = models.Task_Priority.objects.all().order_by('sort')
    serializer_class = serializers.Task_PriorityModelSerializer