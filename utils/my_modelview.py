from rest_framework.response import Response

class MyModelViewSet:

    def get_myinstance(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, list):
            pks = []
            for dic in request_data:
                pk = dic.pop('pk', None)
                if pk:
                    pks.append(pk)
                else:
                    return '数据有误'
        else:
            return '数据有误'
        objs = []
        objs2 = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                obj = self.queryset.get(deptid=pk)
                objs.append(obj)
                new_request_data.append(request_data[index])
            except:
                print('报错')
                continue
        print(objs)
        # print(objs2)
        print(new_request_data)
        return objs, new_request_data