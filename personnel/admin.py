from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group

from . import models
# Register your models here.
class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'mobile', 'email',
                       'gender', ),
        }),
    )

admin.site.register(models.User, MyUserAdmin)
admin.site.register(models.Structure)