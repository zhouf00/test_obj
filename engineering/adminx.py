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
xadmin.site.register(models.Facility)
xadmin.site.register(models.FacilityCollector)
xadmin.site.register(models.FacilitySensor)
xadmin.site.register(models.Machine)
xadmin.site.register(models.Collector)
xadmin.site.register(models.Sensor)
xadmin.site.register(models.Server)
xadmin.site.register(models.CPU)
xadmin.site.register(models.RAM)
xadmin.site.register(models.Disk)
xadmin.site.register(models.NIC)
xadmin.site.register(models.MonitorType)
