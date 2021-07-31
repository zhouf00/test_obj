from rest_framework import serializers

from . import models

class MarketModelSerializer(serializers.ModelSerializer):

    # leaders = serializers.CharField()

    class Meta:
        model = models.Market
        fields = ['id', 'title', 'customer', 'company', 'address', 'designing_institute', 'manufacturer', 'sn',
                  'count', 'estimated_time', 'estimated_amount', 'hit_rate', 'memo', 'create_time','user',
                  'amount', 'traceTime','type', 'coadjutant',
                  # 自定义字段
                  'raterecordList', 'userInfo', 'typeList', 'totalDays'
                  ]


class MarketDeleteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Market
        fields = ['id', 'is_delete']


class MarketUpdateRateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Market
        fields = ['id', 'hit_rate', 'traceTime', 'amount']


class MarketTraceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MarketTrace
        fields = ['id', 'hit_rate', 'content', 'market','user', 'create_time',
                  'userInfo']


class LinkmanModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Linkman
        fields = '__all__'


class RateRecordModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RateRecord
        fields = '__all__'
        extra_kwargs = {
            'hit_rate': {
                'required': False
            },
        }


class MarketHistoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MarketHistory
        fields = ['id','user', 'amount', 'estimated_amount']
