from django.db import models
from django.contrib.auth.models import AbstractUser
from authority.models import Roles


# Create your models here.
class UserProfile(AbstractUser):
    """
    用户信息
    """
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="male",
                              verbose_name="性别")
    mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    email = models.EmailField(max_length=100, verbose_name="邮箱", blank=True)
    picture = models.ImageField(upload_to="image/%Y/%m", default="image/default.jpg", max_length=100, null=True,
                                blank=True)
    department = models.ForeignKey("Structure", null=True, blank=True, verbose_name="部门", on_delete=models.CASCADE)
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, verbose_name="上级主管", on_delete=models.SET_NULL)
    role = models.ManyToManyField("authority.Roles", verbose_name="角色", blank=True)
    joined_date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name="入职日期")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class Structure(models.Model):
    """
    组织架构
    """
    type_choices = (("firm", "公司"), ("department", "部门"))
    title = models.CharField(max_length=60, verbose_name="名称")
    code = models.CharField(max_length=20, verbose_name="代码", null=True, blank=True)  # 1.1.0
    info = models.TextField(default="", verbose_name="描述")
    type = models.CharField(max_length=20, choices=type_choices, default="department", verbose_name="类型")
    position = models.CharField(max_length=50, verbose_name="位置", null=True, blank=True)  # 1.1.0
    phone = models.CharField(max_length=20, verbose_name="电话", null=True, blank=True)  # 1.1.0

    # 1.1.0
    principal = models.ForeignKey("UserProfile", null=True, blank=True, verbose_name="负责人", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="父类架构", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
