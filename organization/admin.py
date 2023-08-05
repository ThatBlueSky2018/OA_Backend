from django.contrib import admin
from .models import UserProfile, Structure


# Register your models here.
class UserProfileRoleInline(admin.TabularInline):
    model = UserProfile.role.through  # 多对多关系生成的中间表模型
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserProfileRoleInline]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Structure)
