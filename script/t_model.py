# Django脚本化启动
import os, django
from django.db.models import Count, Sum
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_obj.settings')
django.setup()

from engineering.models import Project, Manufacturer
from personnel import models
from rbac.models import Menu, Auth
from product import models as product_models
from APPS.crm import models as crm_models

##############
# 项目管理查询
##############
project = Project.objects.filter(area=1).order_by('-update_time')
# print(len(project))

##############
# 销售管理查询
##############
import datetime
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
print(crm_models.Market.objects.filter(user__department=3))

# 历史记录
# print(datetime.datetime.strptime('2020/12/20','%Y/%m/%d'))
# print(crm_models.MarketHistory.objects.annotate().filter(date__year='2020',date__month='11'))
q = crm_models.MarketHistory.objects.filter(date__year='2020',date__month='12').aggregate(sum_0=Sum('rate_0'))  # 求和
# print(q)
time = datetime.datetime.now()
# print(crm_models.MarketHistory.objects.filter(date__year=time.strftime('%Y'),date__month=time.strftime('%m'),date__day=time.strftime('%d')))
#
print(crm_models.MarketHistory.objects.filter(user__department=4).values('user_id'))