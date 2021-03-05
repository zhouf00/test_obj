import datetime
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count

from . import models, serializers, filters
from personnel.models import User,Structure
from utils.response import APIResponse
from utils.pagenations import MyPageNumberPagination


class MarketViewSet(ModelViewSet):

    queryset = models.Market.objects.filter(is_delete=False).order_by('-amount')
    serializer_class = serializers.MarketModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.MarketFilter
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
                self.queryset = self.queryset.filter(Q(user__username__in=self.request.user.deptmembers[0])|Q(coadjutant=self.request.user.id)).distinct()
            else:
                # print('你不是部门领导')
                self.isleader = False
                self.queryset = self.queryset.filter(Q(user=self.request.user.id)|Q(coadjutant=self.request.user.id)).distinct()
        return self.queryset

    def create(self, request, *args, **kwargs):
        #
        request.data['traceTime'] = datetime.datetime.today()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        time = datetime.datetime.today()
        # 创建命中率
        rate_data = {
            'hit_rate': 0.0,
            'start_time': time,
            'market': serializer.data['id']
        }
        rate_ser = serializers.RateRecordModelSerializer(data=rate_data)
        rate_ser.is_valid(raise_exception=True)
        rate_ser.save()

        return APIResponse(
            data_msg='create ok',
            results=serializer.data,
            headers=headers,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['isleader'] = self.isleader
        return APIResponse(results=data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(results=serializer.data)


class MarketDeleteViewSet(ModelViewSet):
    queryset = models.Market.objects.filter(is_delete=False).order_by('-amount')
    serializer_class = serializers.MarketDeleteModelSerializer


class MarketTraceViewSet(ModelViewSet):

    queryset = models.MarketTrace.objects.all().order_by('-create_time')
    serializer_class = serializers.MarketTraceModelSerializer

    filter_class = filters.MarketTraceFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        super().create(request, args, kwargs)
        data = request.data
        market_obj = models.Market.objects.filter(id=data['market'])

        old_rate = market_obj.first().hit_rate
        new_rate = float(data['hit_rate'])
        # print(data['market'])
        # print(old_rate, type(old_rate))
        # print(new_rate,type(new_rate))

        time = datetime.datetime.today()
        # 判断命中率是否变化
        if old_rate == new_rate:
            # 不更新
            pass
        else:
            # 更新
            # 查询新旧命中率obj
            old_rate_id = models.RateRecord.objects.filter(market=data['market'],hit_rate=old_rate)
            new_rate_id = models.RateRecord.objects.filter(market=data['market'],hit_rate=new_rate)
            # print(old_rate_id, new_rate_id)

            # 旧的更新
            old_rate_data = old_rate_id.values()[0]
            old_data = {
                'end_time': time,
                'days': old_rate_data['days']+(time - old_rate_data['start_time']).days
            }
            old_rate_ser = serializers.RateRecordModelSerializer(instance=old_rate_id.first(), data=old_data)
            old_rate_ser.is_valid(raise_exception=True)
            old_rate_ser.save()

            # 新的创建或更新
            if new_rate_id:
                new_rate_data = {
                    'start_time': time,
                    'end_time': None
                }
                rate_ser = serializers.RateRecordModelSerializer(instance=new_rate_id.first(), data=new_rate_data)
            else:
                new_rate_data = {
                    'market':market_obj.first().id,
                    'hit_rate': new_rate,
                    'start_time': time
                }
                rate_ser = serializers.RateRecordModelSerializer(data=new_rate_data)
            rate_ser.is_valid(raise_exception=True)
            rate_ser.save()

        # 更新商机中的hit_rate
        if new_rate != 1 or market_obj.first().hit_rate != 1:
            market_data = {
                'hit_rate': new_rate,
                'traceTime': time,
                'amount': round(market_obj.first().estimated_amount*new_rate, 2)
            }
            market_ser = serializers.MarketUpdateRateModelSerializer(instance=market_obj.first(), data=market_data)
            market_ser.is_valid(raise_exception=True)
            market_ser.save()

        return APIResponse(
            data_msg='create ok',
            results=request.data
        )


class LinkmanViewSet(ModelViewSet):

    queryset = models.Linkman.objects.all().order_by('-update_time')
    serializer_class = serializers.LinkmanModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.LinkmanFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]


class RateRecordViewSet(ModelViewSet):
    queryset = models.RateRecord.objects.all()
    serializer_class = serializers.RateRecordModelSerializer


class MarketHistoryViewSet(ModelViewSet):

    queryset = models.MarketHistory.objects.all()
    serializer_class = serializers.MarketHistoryModelSerializer

    filter_class = filters.MarketHistoryFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def get_queryset(self):
        # # 拿到管理员身份
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
                self.queryset = self.queryset.filter(user__username__in=self.request.user.deptmembers[0]).distinct()
            else:
                # print('你不是部门领导')
                self.isleader = False
                self.queryset = self.queryset.filter(user=self.request.user.id).distinct()
        return self.queryset

    def list(self, request, *args, **kwargs):
        query_data = request.query_params
        date = datetime.datetime.now()
        queryset = self.filter_queryset(self.get_queryset())
        if 'start_time' in query_data or 'end_time' in query_data:
            pass
        else:
            queryset = queryset.filter(date__year=date.strftime('%Y'))
        res_list = []
        users = queryset.values('user', 'user__name').distinct()
        for user in users:
            user_queryset = queryset.filter(user=user['user'])
            performance = user_queryset.aggregate(performance=Sum('rate_100'))['performance']
            if performance:
                performance = round(performance, 2)
            res_list.append({
                'name': user['user__name'],
                'performance': performance,
                'markethistoryInfo': self.add_date(user_queryset)
            })
        return APIResponse(
            results=res_list
        )

    def add_date(self, obj):
        months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        res_dict = {}
        for month in months:
            if obj.filter(date__month=month):
                res_dict[month+'月'] = obj.filter(date__month=month).values()[0]
            else:
                res_dict[month + '月'] = {}
        return res_dict


class AnnalsViewSet(APIView):

    queryset = models.MarketHistory.objects.all()

    def get_queryset(self):
        # # 拿到管理员身份
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
                self.queryset = self.queryset.filter(user__username__in=self.request.user.deptmembers[0]).distinct()
            else:
                # print('你不是部门领导')
                self.isleader = False
                self.queryset = self.queryset.filter(user=self.request.user.id).distinct()
        return self.queryset

    def get(self, request, *args, **kwargs):
        request_user = request.query_params
        queryset = self.get_queryset()

        date = datetime.datetime.now()
        users_obj = User.objects.all()
        # print(request_user)
        if 'sw' in request_user and request_user['sw'] == 'true':
            reload = True
        else:
            reload = False
        # 每日更新
        rate_dict = {'rate_0': 0, 'rate_025': 0.25, 'rate_050': 0.5, 'rate_075': 0.75, 'rate_100': 1}
        # dict1 = {'amount':0, 'estimated_amount': 0}
        queryset_month = queryset.filter(date__year=date.strftime('%Y'), date__month=date.strftime('%m'))
        print(queryset_month[0].date.strftime('%Y%m%d'))
        if reload or not queryset_month.values() or queryset_month[0].date.strftime('%Y%m%d') != date.strftime('%Y%m%d'):
            # print('更新')
            markets_obj = models.Market.objects.filter(traceTime__year=date.strftime('%Y'),
                                                       traceTime__month=date.strftime('%m'),)
            users = markets_obj.exclude(user=None).values('user').distinct()
            for user in users:
                dict1 = {'amount': 0, 'estimated_amount': 0}
                # 获取未删除的项目
                market_obj = markets_obj.filter(user__id=user['user'], is_delete=False)
                user_obj = users_obj.filter(id=user['user'])
                if user_obj:
                    for key, value in rate_dict.items():
                        tmp = self.rate_save(value, market_obj)
                        if tmp:
                            dict1['estimated_amount'] += tmp.pop('estimated_amount')
                            dict1['amount'] += tmp.pop('amount')
                            dict1.update(tmp)
                    dict1.update({'date': date})
                    # # print(user_obj[0], dict1)
                    models.MarketHistory.objects.filter(
                        date__year=date.strftime('%Y'),
                        date__month=date.strftime('%m')
                    ).update_or_create(
                        user=user_obj[0],
                        defaults=dict1
                    )

        # 查询
        if 'department' in request_user:
            queryset = queryset.filter(user__department=request_user['department'])
        else:
            pass
        if 'user' in request_user:
            queryset = queryset.filter(user__id=int(request_user['user']))
        else:
            pass
        months = ['1','2', '3','4','5', '6', '7','8','9', '10', '11', '12']
        annals_list = []
        tmp_chain = 0
        query = queryset.filter(date__year=date.strftime('%Y'))
        for month in months:
            dict1 = query.filter(date__month=month).aggregate(
                rate_0=Sum('rate_0'), rate_0_t=Sum('rate_0_t'),
                rate_025=Sum('rate_025'), rate_025_t=Sum('rate_025_t'),
                rate_050=Sum('rate_050'), rate_050_t=Sum('rate_050_t'),
                rate_075=Sum('rate_075'), rate_075_t=Sum('rate_075_t'),
                rate_100=Sum('rate_100'), rate_100_t=Sum('rate_100_t'),
                estimated_amount=Sum('estimated_amount'),
                amount=Sum('amount')
                )
            dict1.update({'date': month+'月'})
            if dict1['amount']:
                dict1['chain'] = dict1['amount']-tmp_chain
                tmp_chain = dict1['amount']
            annals_list.append(dict1)
        return APIResponse(
            results=annals_list
        )

    # 分类保存
    def rate_save(self, r, obj):
        comm = 'estimated_amount'
        if r == 0:
            res = obj.filter(hit_rate=r).aggregate(
                rate_0=Sum(comm), rate_0_t=Count(comm),
                amount=Sum('amount'), estimated_amount=Sum(comm)
            )
        elif r == 0.25:
            res = obj.filter(hit_rate=r).aggregate(
                rate_025=Sum(comm), rate_025_t=Count(comm),
                amount=Sum('amount'), estimated_amount=Sum(comm)
            )
        elif r == 0.5:
            res = obj.filter(hit_rate=r).aggregate(
                rate_050=Sum(comm), rate_050_t=Count(comm),
                amount=Sum('amount'), estimated_amount=Sum(comm)
            )
        elif r == 0.75:
            res = obj.filter(hit_rate=r).aggregate(
                rate_075=Sum(comm), rate_075_t=Count(comm),
                amount=Sum('amount'), estimated_amount=Sum(comm)
            )
        elif r == 1:
            res = obj.filter(hit_rate=r).aggregate(
                rate_100=Sum(comm), rate_100_t=Count(comm),
                amount=Sum('amount'), estimated_amount=Sum(comm)
            )
        else:
            res = {}
        #  对None进行转换
        # print(res)
        if 'amount' in res and not res['amount']:
            res['amount'] = 0.0
        if 'estimated_amount' in res and not res['estimated_amount']:
            res['estimated_amount'] = 0.0
        return res
