from django.contrib import admin
from .models import Equipment, Equ_States, Repair_Manage, Repair_Accept, Repair_Schedule, Repair_Request, Repair_Off_Req, Order_Ids
#
# Register your models here.
admin.site.register(Equipment)
admin.site.register(Equ_States)
admin.site.register(Repair_Manage)
admin.site.register(Repair_Accept)
admin.site.register(Repair_Schedule)
admin.site.register(Repair_Request)
admin.site.register(Repair_Off_Req)
admin.site.register(Order_Ids)
