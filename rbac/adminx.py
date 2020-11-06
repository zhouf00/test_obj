import xadmin

from . import models

xadmin.site.register(models.Menu)
xadmin.site.register(models.Auth)