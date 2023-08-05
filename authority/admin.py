from django.contrib import admin
from .models import Menu, Roles


# Register your models here.

class RoleMenuInline(admin.TabularInline):
    model = Roles.permission.through  # 多对多关系生成的中间表模型
    extra = 1


class RoleAdmin(admin.ModelAdmin):
    inlines = [RoleMenuInline]


admin.site.register(Menu)
admin.site.register(Roles, RoleAdmin)
