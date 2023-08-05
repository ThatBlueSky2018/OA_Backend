from django.db import models
from django.contrib.auth.models import Group, Permission


# Create your models here.
class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(max_length=32, unique=True, verbose_name="菜单名")
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="父菜单", on_delete=models.SET_NULL)
    is_top = models.BooleanField(default=False, verbose_name="首页显示")  # 是否是一级菜单
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="编码")
    url = models.CharField(max_length=128, unique=True, null=True, blank=True)

    def __str__(self):
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    @classmethod
    def getMenuByRequestUrl(cls, url):
        ret = dict(menu=Menu.objects.get(url=url))
        return ret


class Roles(models.Model):
    """
    角色：绑定菜单
    """
    title = models.CharField(max_length=32, verbose_name="角色名称")
    responsibility = models.TextField(default="", verbose_name="职责")
    permission = models.ManyToManyField(Menu, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)  # 与系统权限表相关联

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
