import datetime

from django.db import models
from organization.models import UserProfile
from organization.models import Structure


# Create your models here.
class Equipment(models.Model):
    """
    设备信息表
    """
    code = models.CharField(max_length=15, verbose_name="设备编号")
    name = models.CharField(max_length=10, verbose_name="设备名称")
    type = models.CharField(max_length=10, verbose_name="设备型号")
    manufacture = models.CharField(max_length=10, verbose_name="生产商")
    info = models.TextField(max_length=300, blank=True, null=True, verbose_name="设备描述")
    picture = models.ImageField(blank=True, null=True, verbose_name="设备图片")

    class Meta:
        verbose_name = "设备信息"
        verbose_name_plural = verbose_name


class Equ_States(models.Model):
    """
    设备状态表
    """
    code = models.CharField(max_length=15, verbose_name="设备编号")
    purchaser = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING,
                                  related_name="equipments", verbose_name="采购人")
    use_dep = models.ForeignKey(Structure, on_delete=models.DO_NOTHING, related_name="equipments", verbose_name="使用部门")
    life_limit = models.IntegerField(verbose_name="使用年限")
    time_touse = models.DateTimeField(verbose_name="投用时间")
    status = models.CharField(max_length=10, verbose_name="目前状态")

    class Meta:
        verbose_name = "设备状态"
        verbose_name_plural = verbose_name


class Repair_Schedule(models.Model):
    """
    设备维修计划表
    """
    orderid = models.CharField(max_length=15, verbose_name="单号")
    code = models.CharField(max_length=10, verbose_name="设备编号")
    name = models.CharField(max_length=10, verbose_name="设备名称")
    type = models.CharField(max_length=10, verbose_name="检修类别")
    info = models.TextField(max_length=100, verbose_name="主要检修内容")
    start = models.DateTimeField(verbose_name="预计开始日期")
    end = models.DateTimeField(verbose_name="预计结束日期")
    cost = models.IntegerField(verbose_name="预计检修费用")
    date = models.DateTimeField(verbose_name="制定日期")

    class Meta:
        verbose_name = "设备维修计划表"
        verbose_name_plural = verbose_name


class Repair_Request(models.Model):
    """
    设备维修申请表
    """
    orderid = models.CharField(max_length=15, verbose_name="单号")
    code = models.CharField(max_length=10, verbose_name="设备编号")
    name = models.CharField(max_length=10, verbose_name="设备名称")
    type = models.CharField(max_length=10, verbose_name="维修类型")
    erro =models.CharField(max_length=100,verbose_name='故障说明')
    info = models.TextField(max_length=100, verbose_name="维修说明")
    start = models.DateTimeField(verbose_name="预计开始日期")
    end = models.DateTimeField(verbose_name="预计结束日期")
    cost = models.IntegerField(verbose_name="预计检修费用")
    date = models.DateTimeField(verbose_name="申请日期")

    class Meta:
        verbose_name = "设备维修申请表"
        verbose_name_plural = verbose_name


class Repair_Off_Req(models.Model):
    """
    设备关停申请表
    """
    orderid = models.CharField(max_length=15, verbose_name="单号")
    code = models.CharField(max_length=10, verbose_name="设备编号")
    name = models.CharField(max_length=10, verbose_name="设备名称")
    type = models.CharField(max_length=10, verbose_name="关停类型")
    info = models.TextField(max_length=100, verbose_name="关停原因")
    start = models.DateTimeField(verbose_name="预计开始日期")
    end = models.DateTimeField(verbose_name="预计结束日期")
    date = models.DateTimeField(verbose_name="申请日期")

    class Meta:
        verbose_name = "设备关停申请表"
        verbose_name_plural = verbose_name


class Repair_Accept(models.Model):
    """
    设备维修验收表
    """
    orderid = models.CharField(max_length=15, verbose_name="单号")
    code = models.CharField(max_length=10, verbose_name="设备编号")
    name = models.CharField(max_length=10, verbose_name="设备名称")
    type = models.CharField(max_length=10,verbose_name='验收类型')
    info = models.TextField(max_length=100, verbose_name="维修记录")
    date = models.DateTimeField(verbose_name="验收日期")

    class Meta:
        verbose_name = "设备维修验收表"
        verbose_name_plural = verbose_name


class Repair_Manage(models.Model):
    """
    设备维修管理表
    """
    orderid = models.CharField(max_length=15, verbose_name="单号")
    type = models.CharField(max_length=10, verbose_name="类型")

    # 0待提交，1待审批，2已审批，3退回，4待验收，5已验收
    status = models.IntegerField(verbose_name="状态")

    maker = models.ForeignKey(UserProfile, verbose_name="发起人", related_name="make_orders",
                              on_delete=models.DO_NOTHING)
    approver1 = models.ForeignKey(UserProfile, verbose_name="审批人1", related_name="approve_orders1",
                                  on_delete=models.DO_NOTHING,null=True,blank=True)
    date1 = models.DateTimeField(verbose_name="审批日期1")
    approver2 = models.ForeignKey(UserProfile, verbose_name="审批人2", related_name="approve_orders2",
                                  on_delete=models.DO_NOTHING,null=True,blank=True)
    date2 = models.DateTimeField(verbose_name="审批日期2")
    acceptor = models.ForeignKey(UserProfile, verbose_name="验收人", related_name="accept_orders",
                                 on_delete=models.DO_NOTHING,null=True,blank=True)
    memo = models.TextField(verbose_name="备注",null=True,blank=True)

    class Meta:
        verbose_name = "设备维修管理表"
        verbose_name_plural = verbose_name


class Order_Ids(models.Model):
    """
    记录某一天各种工单生成的数量
    """
    date = models.DateField()
    RP = models.IntegerField()  # 设备维修计划表数量
    RR = models.IntegerField()  # 设备维修申请表数量
    OFF = models.IntegerField()  # 设备关停申请表数量
    RA = models.IntegerField()  # 设备维修验收表数量

    class Meta:
        verbose_name = "每日工单数量"
        verbose_name_plural = verbose_name

