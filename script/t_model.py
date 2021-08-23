# Django脚本化启动
import os, django
import time,datetime
from itertools import chain
from django.db.models import Count, Sum, Q
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_obj.settings')
django.setup()

from engineering.models import Project, Manufacturer, ProjectStatusTime, ProjectStatus,ProjectTrace,Outsourcer
from personnel import models as personnel_models
from rbac.models import Menu, Auth
from product import models as product_models
from APPS.crm import models as crm_models
from mlr import models as mlr_models

##############
# 项目管理查询
##############

# project = Project.objects.filter(area=1).order_by('-update_time')
# print(Project.objects.filter(begin_time__year='2021'))
# print(Project.objects.filter(status_))
# print(ProjectStatusTime.objects.filter(status_id=1))
# print(time.strftime("%Y", time.localtime(int('1577808000000')/1000)))
# p = list(Project.objects.values('id', 'sn', 'serial', 'begin_time', 'type__title'))
# print(p)
# type = {
#     '水泥': '06',
#     '电力石化': '02',
#     '轨交': '03',
#     '煤炭': '05',
#     '油气': '07',
#     '风电-陆上': '01',
#     '风电-海上': '01',
#     '风电': '01',
# }
# for var in p:
#     if var['begin_time']:
#         p_time = var['begin_time'].strftime('%y%m')
#     else:
#         p_time = ''
#     if var['sn']:
#         sn = var['sn']
#         if 'H' in sn:
#             t_sn = '0H'+ sn[-4:]
#             Project.objects.filter(id=var['id']).update(sn=p_time+t_sn, serial=t_sn)
#         else:
#             t_sn = type[var['type__title']]+sn[-4:]
#
#             Project.objects.filter(id=var['id']).update(sn=p_time+t_sn, serial=t_sn)
        #
        # print(sn, sn[-4:],p_time)

# print(p.filter(Q(builders__isnull=False) |Q(priority__isnull=False)).values('priority__title', 'status__title', 'builders__name'))
# tag_list = list(ProjectStatus.objects.values('title'))
# print(tag_list)
# for var in tag_list:
#     var['count'] = p.filter(status__title=var['title']).count()
#     print(var)
# tag_list.append({'title':'全部'})
date = datetime.datetime.now()
# print(ProjectTrace.objects.filter(project=5).values('subscriber'))
# print(Outsourcer.objects.filter(contract__project=4))
# print(ProjectTrace.objects.filter(
#             create_time__year=date.strftime('%Y'),
#             create_time__month=date.strftime('%m'),
#             create_time__day=date.strftime('%d'),
#             worklog__isnull=False
#     ).values('content'))

# 添加销售负责人
f1 = ['明阳','上海电气','运达','东方电气','华东院']
u1 = '鞠文龙'
f2 = ['联合动力', '中车风电', '金风']
u2 = '陈欢'
# p = Project.objects.filter(manufacturers__title__in=f2).values('id')
# print(len(p))
# u = [v['id'] for v in personnel_models.User.objects.filter(name=u2).values()]
# print(u)

# 添加诊断负责人
f3 = ['联合动力']
u3 = '黄朝'
f4 = ['运达']
u4 = '肖丹'
u5 = '王忠建'
u6 = '蔡志雄'
# p1 = [v['id'] for v in Project.objects.filter(manufacturers__title__in=f3).values('id')]
# p2 = [v['id'] for v in Project.objects.exclude(manufacturers__title__in=f4+f3).values('id')]
# p3 = [v['id'] for v in Project.objects.values('id')]
# print(len(p3))
# print(personnel_models.User.objects.filter(name=u5))
# personnel_models.User.objects.filter(name=u3).first().diagnosis_project.set(p1)

# 添加订阅
# p4 = Project.objects.filter(priority__isnull=False)     # 所有有优先级项目
# print(len(p4))
# print(personnel_models.User.objects.filter(name='吴炯锋'))
# personnel_models.User.objects.filter(name='吴炯锋').first().collect.set(p4)
# print(Project.objects.filter(priority__isnull=False).filter(collect__name='吴炯锋'))

##############
# 销售管理查询
##############
# print(crm_models.Market.objects.filter(pk=15).first().hit_rate)
# print(crm_models.RateRecord.objects.filter(hit_rate=0.5).values())
# 时间计算
# start = crm_models.RateRecord.objects.filter(market=2).values()[0]['start_time']
# end = datetime.datetime.strptime('2020-12-1 15:30:20','%Y-%m-%d %H:%M:%S')
# print((end-start).days)
# print(crm_models.Market.objects.filter(user__in=[15, 16, 17, 19]))
# print(crm_models.Market.objects.filter(user__username__in=['ZhouWenXing', 'gen', 'ZhangJingJing', 'test1']))
# print(models.User.objects.filter())
# print(models.Structure.objects.filter(deptid__in=[3]).values('id'))
# print(models.DeptToUser.objects.filter(department=3))
# models.DeptToUser.objects.filter(department=3, user__in=['test1','ZhouWenXing']).update(isleader=True)
# obj = crm_models.Market.objects.all()
# users = obj.values('user__name').distinct()
# print(users)
# print(len(obj))
# for user in users:
#     print(obj.filter(user__name=user['user__name']).values('title', 'hit_rate', 'traceTime'))

# department_member = models.User.objects.filter(department__name='销售二部').values('username')
# users = [user['username']  for user in department_member]
# print(users)
# print(crm_models.Market.objects.filter(user__department=3))
# print(crm_models.Market.objects.filter(Q(user=3)| Q(coadjutant=6)).values('title'))

# 历史记录
# print(datetime.datetime.strptime('2020/12/20','%Y/%m/%d'))
# print(crm_models.MarketHistory.objects.annotate().filter(date__year='2020',date__month='11'))
# q = crm_models.MarketHistory.objects.filter(date__year='2020',date__month='12').aggregate(sum_0=Sum('rate_0'))  # 求和
# print(q)
# print(crm_models.MarketHistory.objects.filter(date__year=time.strftime('%Y'),date__month=time.strftime('%m'),date__day=time.strftime('%d')))
#
# print(crm_models.MarketHistory.objects.filter(user__department=4).values('user_id'))

##############
# 人员查询
##############
# user_list = personnel_models.User.objects.filter(project__isnull=True).filter(department__in=[6]).values('project', 'project__name', 'name')
# print(len(user_list))
# for var in user_list:
#     print(var)

# print('人员',personnel_models.User.objects.exclude(is_active=False))
# print(personnel_models.Structure.objects.filter(deptid=))
# print(personnel_models.User.objects.filter(name__contains='吴'))
# print(personnel_models.Structure.objects.filter(parentid__isnull=False))
# print(personnel_models.DeptToUser.objects.filter(department__parentid=101).filter(isleader=True).values('department__name','user__name'))

##############
# 日报功能
##############
date = datetime.datetime.now()
# print(date.strftime('%Y%m%d'))
a = mlr_models.WorkLogs.objects.values()
# print(len(a))
# print(mlr_models.Summary.objects.filter(create_time__year=date.strftime('%Y'), create_time__month=date.strftime('%m'), create_time__day=date.strftime('%d')))

b = mlr_models.WorkStatus.objects.all()
c = mlr_models.OtherEnv.objects.exclude()

# print(mlr_models.Task.objects.filter(subscriber=2).values())
# print('|'.join([v['username'] for v in personnel_models.User.objects.filter(id__in=[2,2,3,3,4,5,7,7]).exclude(username='user3').values('username')]))
# print(mlr_models.Task.objects.filter(executor=2))