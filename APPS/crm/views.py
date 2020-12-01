import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, serializers, filters
from utils.response import APIResponse
from utils.authentications import JWTAuthentication
from utils.pagenations import MyPageNumberPagination
from utils.my_modelview import ProjectUpdateViewSet


class MarketViewSet(ModelViewSet):

    queryset = models.Market.objects.all().order_by('-amount')
    serializer_class = serializers.MarketModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.MarketFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

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

        # 判断命中率是否变化
        if old_rate == new_rate:
            print('不更新')
        else:
            print('更新')
            time = datetime.datetime.today()
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
            market_data = {
                'hit_rate': new_rate,
                'traceTime': time,
                'amount': int(market_obj.first().estimated_amount*new_rate)
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


