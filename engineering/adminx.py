import xadmin

from . import models

class ProjectAdmin(object):
    list_display = ['name', 'address', 'sn', 'status','manufacturers']
    list_filter = ['is_delete',]


class ManufacturerAdmin(object):
    list_display = ['title', 'telephone']


class MachineAdmin(object):
    list_display = ['title', 'manufacturer']

xadmin.site.register(models.Project, ProjectAdmin)
xadmin.site.register(models.Manufacturer, ManufacturerAdmin)
xadmin.site.register(models.Machine)
xadmin.site.register(models.MonitorType)
xadmin.site.register(models.StockFinish)

