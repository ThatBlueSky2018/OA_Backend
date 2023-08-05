from rest_framework.response import Response
from . import serializer
from rest_framework.views import APIView
from . import models
from . import tools
from . import permissions

# Create your views here.
# 设备管理
class showAllEquipment(APIView):
    #permission_classes=[permissions.ViewEquipPermission]
    def get(self, req):
        params = req.query_params
        if 'code' not in params.keys():
            eqpList = models.Equipment.objects.all()
            seri = serializer.equip_serializer(instance=eqpList, many=True)
            return Response(seri.data)
        else:
            eqpList = models.Equipment.objects.filter(code__contains=params['code'])
            seri = serializer.equip_serializer(instance=eqpList, many=True)
            return Response(seri.data)

    def put(self, req):
        code = req.query_params['code']
        theeqp = models.Equipment.objects.filter(code=code)
        if theeqp.count() == 0:
            return Response('没有找到code对应的设备')
        seri = serializer.equip_serializer(data=req.data)
        if seri.is_valid():
            theeqp.update(**seri.validated_data)
            return Response("设备修改成功")
        else:
            return Response(seri.errors)

    def delete(self, req):
        reqlist = req.query_params
        code = reqlist['code']
        row = models.Equipment.objects.filter(code=code)
        if row.count() == 0:
            return Response('没有找到code对应的设备')
        else:
            row.delete()
            return Response('删除成功')


class addEquipment(APIView):
    #permission_classes = [permissions.AddEquipPermission]
    def get(self, req):
        return Response('进入添加页面')

    def post(self, req):
        seri = serializer.equip_serializer(data=req.data)
        if seri.is_valid():
            models.Equipment.objects.create(**seri.validated_data)
            return Response('添加成功')
        else:
            return Response(seri.errors)


# 设备状态管理
class showallstate(APIView):
    #permission_classes = [permissions.ViewStatePermission]
    def get(self, req):
        params = req.query_params
        if "code" not in params.keys():
            statelist = models.Equ_States.objects.all()
            seri = serializer.equip_states_serializer(instance=statelist, many=True)
            return Response(seri.data)
        else:
            code = params['code']
            statelist = models.Equ_States.objects.filter(code__contains=code)
            seri = serializer.equip_states_serializer(instance=statelist, many=True)
            return Response(seri.data)

    def put(self, req):
        code = req.query_params['code']
        theeqp = models.Equ_States.objects.filter(code=code)
        if theeqp.count() == 0:
            return Response('没有找到code对应的设备状态')
        seri = serializer.equip_states_serializer(data=req.data)
        if seri.is_valid():
            theeqp.update(**seri.validated_data)  ##
            return Response('更改{}设备状态成功'.format(code))
        else:
            return Response(seri.errors)

    def delete(self, req):
        reqlist = req.query_params
        code = reqlist['code']
        row = models.Equ_States.objects.filter(code=code)
        if row.count() == 0:
            return Response('没有找到code对应的设备')
        else:
            row.delete()
            return Response('删除成功')


class addstates(APIView):
    #permission_classes = [permissions.AddStatePermission]
    def get(self, req):
        return Response('进入添加页面')

    def post(self, req):
        seri = serializer.equip_states_serializer(data=req.data)
        if seri.is_valid():
            models.Equ_States.objects.create(**seri.validated_data)
            return Response('添加成功')
        else:
            return Response(seri.errors)


# 计划表管理
class showrepair_schedule(APIView):
    #permission_classes = [permissions.ViewSchedulePermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            datas = models.Repair_Manage.objects.filter(orderid__contains="RP").values("orderid", "type", "status")
            for data in datas:
                if data["orderid"].startswith('RP'):
                    info = models.Repair_Schedule.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                else:
                    Response("wrong orderid")
            seri = serializer.info_serializer(instance=datas, many=True)
            return Response(seri.data)
        # 有code参数
        else:
            if "orderid" in params.keys():
                orderid = params['orderid']
                datas = models.Repair_Manage.objects.filter(orderid__contains="RP").filter(
                    orderid__contains=orderid).values("orderid", "type", "status")
                for data in datas:
                    if data["orderid"].startswith('RP'):
                        info = models.Repair_Schedule.objects.filter(orderid=data["orderid"]).values("info").first()
                        data["info"] = info
                    else:
                        Response("wrong orderid")
                seri = serializer.info_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def delete(self, req):
        reqlist = req.query_params
        if "orderid" in reqlist.keys():
            orderid = reqlist['orderid']
            row1 = models.Repair_Schedule.objects.filter(orderid=orderid)
            if row1.count() == 0:
                return Response('没有找到要删除的订单')
            row2 = models.Repair_Manage.objects.filter(orderid=orderid)
            if row2.count() == 0:
                return Response('没有找到要删除的订单')
            row2.delete()
            row1.delete()
            return Response('删除成功')
        else:
            return Response("error")


class addrepair_schedule(APIView):
    #permission_classes = [permissions.AddSchedulePermission]
    def get(self, req):
        data = {}
        data["orderid"] = tools.neworderid.getnextRP()
        data["code"] = ""
        data["name"] = ""
        data["type"] = "维修计划单"
        data["info"] = ""
        data["start"] = tools.fortime.nowdatetime()
        data["end"] = tools.fortime.nowdatetime()
        data["cost"] = 0
        data["date"] = tools.fortime.nowdatetime()
        seri = serializer.repair_schedule_detail_serializer(instance=data)
        return Response(seri.data)

    def post(self, req):
        # url中method参数表示提交或者保存save submit
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "method" in params.keys():
                seri = serializer.repair_schedule_detail_serializer(data=req.data)
                if seri.is_valid():
                    equip = models.Equipment.objects.filter(code=seri.validated_data["code"])
                    if equip.count() == 0:
                        return Response("没有对应设备")
                    else:
                        managedata = {}
                        managedata["orderid"] = seri.validated_data["orderid"]
                        managedata["type"] = "维修计划单"
                        if params['method'] == "save":
                            managedata["status"] = 0
                        else:
                            if params['method'] == "submit":
                                managedata["status"] = 1
                            else:
                                return Response("error")
                        managedata["maker"] =req.auth.user  ##待修改
                        managedata["approver1"] = None
                        managedata["date1"] = tools.fortime.defaulttime()
                        managedata["approver2"] = None
                        managedata["date2"] = tools.fortime.defaulttime()
                        managedata["acceptor"] = None
                        managedata["memo"] = ""
                        #manageseri = serializer.repair_manage_serializer(instance=managedata)
                        models.Repair_Schedule.objects.create(**seri.validated_data)
                        #models.Repair_Manage.objects.create(**manageseri.data)
                        models.Repair_Manage.objects.create(**managedata)
                        models.Order_Ids.objects.all().update(
                        RP=tools.neworderid.getnum(seri.validated_data["orderid"]))
                        return Response('添加成功')
                else:
                    return Response(seri.errors)
            else:
                return Response("error")


class showrepair_scheduledetail(APIView):
    #permission_classes = [permissions.ViewscheduleDetailPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                orderid = params["orderid"]
                datas = models.Repair_Schedule.objects.filter(orderid=orderid)
                seri = serializer.repair_schedule_detail_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def put(self, req):
        # 需要method与orderid参数
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    datas = models.Repair_Schedule.objects.filter(orderid=orderid)
                    if datas.count() == 0:
                        return Response('没有对应订单')
                    else:
                        seri = serializer.repair_schedule_detail_serializer(data=req.data)
                        if seri.is_valid():
                            code = seri.validated_data['code']
                            if models.Equipment.objects.filter(code=code).count() == 0:
                                return Response('没有对应设备')
                            else:
                                if method == "save":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=0, approver1=None,
                                                                                                approver2=None)
                                elif method == "submit":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=1, approver1=None,
                                                                                                approver2=None)
                                else:
                                    return Response("error")
                                return Response("修改成功")
                        else:
                            return Response(seri.errors)
                else:
                    return Response("error")
            else:
                return Response("error")

    def post(self, req):
        # url中method参数确定是接受还是驳回
        # 请求体只有memo信息
        params = req.query_params
        data = req.data
        if "memo" not in data.keys():
            return Response("请求体需要且仅需要给出memo")
        else:
            memo = data["memo"]
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    if models.Repair_Manage.objects.filter(orderid=orderid).count() == 0:
                        return Response('没有对应订单')
                    else:
                        if method == "reject":
                            models.Repair_Manage.objects.filter(orderid=orderid).update(status=3, approver1=None,
                                                                                        approver2=None, memo=memo)
                            return Response("退回成功")
                        else:
                            if method == "accept":
                                approvers = \
                                models.Repair_Manage.objects.filter(orderid=orderid).values("approver1", "approver2")[0]
                                if approvers["approver1"] is None:
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(approver1=req.auth.user,
                                                                                                memo=memo)
                                    return Response("审批成功")
                                else:
                                    if approvers["approver2"] is None:
                                        models.Repair_Manage.objects.filter(orderid=orderid).update(approver2=req.auth.user,
                                                                                                    memo=memo,
                                                                                                    status=2)  ##待修改
                                        return Response("审批成功")
                                    else:
                                        return Response("该订单已被审批通过，无需再次审批")
                            else:
                                return Response("error")
                else:
                    return Response("error")
            else:
                return Response("error")


# 需求表管理
class showrepair_request(APIView):
    #permission_classes = [permissions.ViewRequestPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            datas = models.Repair_Manage.objects.filter(orderid__contains="RR").values("orderid", "type", "status")
            for data in datas:
                if data["orderid"].startswith('RR'):
                    info = models.Repair_Request.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                else:
                    Response("wrong orderid")
            seri = serializer.info_serializer(instance=datas, many=True)
            return Response(seri.data)
        # 有code参数
        else:
            if "orderid" in params.keys():
                orderid = params['orderid']
                datas = models.Repair_Manage.objects.filter(orderid__contains="RR").filter(
                    orderid__contains=orderid).values("orderid", "type", "status")
                for data in datas:
                    if data["orderid"].startswith('RR'):
                        info = models.Repair_Request.objects.filter(orderid=data["orderid"]).values("info").first()
                        data["info"] = info
                    else:
                        Response("wrong orderid")
                seri = serializer.info_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def delete(self, req):
        reqlist = req.query_params
        orderid = reqlist['orderid']
        row = models.Repair_Request.objects.filter(orderid=orderid)
        if row.count() == 0:
            return Response('没有找到要删除的订单')
        row2 = models.Repair_Manage.objects.filter(orderid=orderid)
        if row2.count() == 0:
            return Response('没有找到要删除的订单')
        row2.delete()
        row.delete()
        return Response('删除成功')


class addrepair_request(APIView):
    #permission_classes = [permissions.AddRequestPermission]
    def get(self, req):
        data = {}
        data["orderid"] = tools.neworderid.getnextRR()
        data["code"] = ""
        data["name"] = ""
        data["type"] = "维修申请单"
        data["erro"] = ""
        data["info"] = ""
        data["start"] = tools.fortime.nowdatetime()
        data["end"] = tools.fortime.nowdatetime()
        data["cost"] = 0
        data["date"] = tools.fortime.nowdatetime()
        seri = serializer.repair_request_detail_serializer(instance=data)
        return Response(seri.data)

    def post(self, req):
        # url中method参数表示提交或者保存
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "method" in params.keys():
                seri = serializer.repair_request_detail_serializer(data=req.data)
                if seri.is_valid():
                    if seri.is_valid():
                        equip = models.Equipment.objects.filter(code=seri.validated_data["code"])
                        if equip.count() == 0:
                            return Response("没有对应设备")
                        else:
                            managedata = {}
                            managedata["orderid"] = seri.validated_data["orderid"]
                            managedata["type"] = "维修申请单"
                            if params['method'] == "save":
                                managedata["status"] = "0"
                            else:
                                if params['method'] == "submit":
                                    managedata["status"] = "1"
                                else:
                                    return Response("error")
                            managedata["maker"] =req.auth.user  ##待修改
                            managedata["approver1"] = None
                            managedata["date1"] = tools.fortime.defaulttime()
                            managedata["approver2"] = None
                            managedata["date2"] = tools.fortime.defaulttime()
                            managedata["acceptor"] = None
                            managedata["memo"] = ""
                            #manageseri = serializer.repair_manage_serializer(instance=managedata)
                            models.Repair_Request.objects.create(**seri.validated_data)
                            #models.Repair_Manage.objects.create(**manageseri.data)
                            models.Repair_Manage.objects.create(**managedata)
                            models.Order_Ids.objects.all().update(
                                RR=tools.neworderid.getnum(seri.validated_data["orderid"]))
                            return Response('添加成功')
                else:
                    return Response(seri.errors)
            else:
                return Response("error")


class showrepair_requestdetail(APIView):
    #permission_classes = [permissions.ViewRequestDetailPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                orderid = params["orderid"]
                datas = models.Repair_Request.objects.filter(orderid=orderid)
                seri = serializer.repair_request_detail_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def put(self, req):
        # 需要method与orderid参数
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    datas = models.Repair_Request.objects.filter(orderid=orderid)
                    if datas.count() == 0:
                        return Response('没有对应订单')
                    else:
                        seri = serializer.repair_request_detail_serializer(data=req.data)
                        if seri.is_valid():
                            code = seri.validated_data['code']
                            if models.Equipment.objects.filter(code=code).count() == 0:
                                return Response('没有对应设备')
                            else:
                                if method == "save":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=0, approver1=None,
                                                                                                approver2=None)
                                elif method == "submit":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=1, approver1=None,
                                                                                                approver2=None)
                                else:
                                    return Response("error")
                                return Response("修改成功")
                        else:
                            return Response(seri.errors)
                else:
                    return Response("error")
            else:
                return Response("error")

    def post(self, req):
        # url中method参数确定是接受还是驳回
        params = req.query_params
        data = req.data
        if "memo" not in data.keys():
            return Response("请求体需要且仅需要给出memo")
        else:
            memo = data["memo"]
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    if models.Repair_Manage.objects.filter(orderid=orderid).count() == 0:
                        return Response('没有对应订单')
                    else:
                        if method == "reject":
                            models.Repair_Manage.objects.filter(orderid=orderid).update(status=3, approver1=None,
                                                                                        approver2=None, memo=memo)
                            return Response("退回成功")
                        else:
                            if method == "accept":
                                approvers = models.Repair_Manage.objects.filter(orderid=orderid).values("approver1",
                                                                                                        "approver2")[0]

                                if approvers["approver1"] is None:
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(approver1=req.auth.user)  ##待修改
                                    return Response("审批成功")
                                else:
                                    if approvers["approver2"] is None:
                                        models.Repair_Manage.objects.filter(orderid=orderid).update(approver2=req.auth.user,
                                                                                                    status=2)  ##待修改
                                        return Response("审批成功")
                                    else:
                                        return Response("该订单已被审批通过，无需再次审批")
                            else:
                                return Response("error")
                else:
                    return Response("error")
            else:
                return Response("error")


# 关停表管理
class showrepair_off_req(APIView):
    #permission_classes = [permissions.ViewOffPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            datas = models.Repair_Manage.objects.filter(orderid__contains="OFF").values("orderid", "type", "status")
            for data in datas:
                if data["orderid"].startswith('OFF'):
                    info = models.Repair_Off_Req.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                else:
                    Response("wrong orderid")
            seri = serializer.info_serializer(instance=datas, many=True)
            return Response(seri.data)
        # 有code参数
        else:
            if "orderid" in params.keys():
                orderid = params['orderid']
                datas = models.Repair_Manage.objects.filter(orderid__contains="OFF").filter(
                    orderid__contains=orderid).values("orderid", "type", "status")
                for data in datas:
                    if data["orderid"].startswith('OFF'):
                        info = models.Repair_Off_Req.objects.filter(orderid=data["orderid"]).values("info").first()
                        data["info"] = info
                    else:
                        Response("wrong orderid")
                seri = serializer.info_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def delete(self, req):
        reqlist = req.query_params
        orderid = reqlist['orderid']
        row = models.Repair_Off_Req.objects.filter(orderid=orderid)
        if row.count() == 0:
            return Response('没有找到要删除的订单')
        row2 = models.Repair_Manage.objects.filter(orderid=orderid)
        if row2.count() == 0:
            return Response('没有找到要删除的订单')
        row2.delete()
        row.delete()
        return Response('删除成功')


class addrepair_off_req(APIView):
    #permission_classes = [permissions.AddOffPermission]
    def get(self, req):
        data = {}
        data["orderid"] = tools.neworderid.getnextOFF()
        data["code"] = ""
        data["name"] = ""
        data["type"] = "关停申请单"
        data["info"] = ""
        data["start"] = tools.fortime.nowdatetime()
        data["end"] = tools.fortime.nowdatetime()
        data["cost"] = 0
        data["date"] = tools.fortime.nowdatetime()
        seri = serializer.repair_request_detail_serializer(instance=data)
        return Response(seri.data)

    def post(self, req):
        # url中method参数表示提交或者保存
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "method" in params.keys():
                seri = serializer.repair_off_req_detail_serializer(data=req.data)
                if seri.is_valid():
                    equip = models.Equipment.objects.filter(code=seri.validated_data["code"])
                    if equip.count() == 0:
                        return Response("没有对应设备")
                    else:
                        managedata = {}
                        managedata["orderid"] = seri.validated_data["orderid"]
                        managedata["type"] = "关停申请单"
                        if params['method'] == "save":
                            managedata["status"] = "0"
                        else:
                            if params['method'] == "submit":
                                managedata["status"] = "1"
                            else:
                                return Response("error")
                        managedata["maker"] =req.auth.user  ##待修改
                        managedata["approver1"] = None
                        managedata["date1"] = tools.fortime.defaulttime()
                        managedata["approver2"] = None
                        managedata["date2"] = tools.fortime.defaulttime()
                        managedata["acceptor"] = None
                        managedata["memo"] = ""
                        #manageseri = serializer.repair_manage_serializer(instance=managedata)
                        models.Repair_Off_Req.objects.create(**seri.validated_data)
                        #models.Repair_Manage.objects.create(**manageseri.data)
                        models.Repair_Manage.objects.create(**managedata)
                        models.Order_Ids.objects.all().update(
                            OFF=tools.neworderid.getnum(seri.validated_data["orderid"]))
                        return Response('添加成功')
                else:
                    return Response(seri.errors)
            else:
                return Response("error")


class showrepair_off_reqdetail(APIView):
    #permission_classes = [permissions.ViewOffDetailPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                orderid = params["orderid"]
                datas = models.Repair_Off_Req.objects.filter(orderid=orderid)
                seri = serializer.repair_off_req_detail_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def put(self, req):
        # 需要method与orderid参数
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    datas = models.Repair_Off_Req.objects.filter(orderid=orderid)
                    if datas.count() == 0:
                        return Response('没有对应订单')
                    else:
                        seri = serializer.repair_off_req_detail_serializer(data=req.data)
                        if seri.is_valid():
                            code = seri.validated_data['code']
                            if models.Equipment.objects.filter(code=code).count() == 0:
                                return Response('没有对应设备')
                            else:
                                if method == "save":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=0, approver1=None,
                                                                                                approver2=None)
                                elif method == "submit":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=1, approver1=None,
                                                                                                approver2=None)
                                else:
                                    return Response("error")
                                return Response("修改成功")
                        else:
                            return Response(seri.errors)
                else:
                    return Response("error")
            else:
                return Response("error")

    def post(self, req):
        # url中method参数确定是接受还是驳回
        params = req.query_params
        data = req.data
        if "memo" not in data.keys():
            return Response("请求体需要且仅需要给出memo")
        else:
            memo = data["memo"]
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    if models.Repair_Manage.objects.filter(orderid=orderid).count() == 0:
                        return Response('没有对应订单')
                    else:
                        if method == "reject":
                            models.Repair_Manage.objects.filter(orderid=orderid).update(status=3, approver1=None,
                                                                                        approver2=None, memo=memo)
                            return Response("退回成功")
                        else:
                            if method == "accept":
                                approvers = models.Repair_Manage.objects.filter(orderid=orderid).values("approver1",
                                                                                                        "approver2")[0]
                                if approvers["approver1"] is None:
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(approver1=req.auth.user)  ##待修改
                                    return Response("审批成功")
                                else:
                                    if approvers["approver2"] is None:
                                        models.Repair_Manage.objects.filter(orderid=orderid).update(approver2=req.auth.user,
                                                                                                    status=2)  ##待修改
                                        return Response("审批成功")
                                    else:
                                        return Response("该订单已被审批通过，无需再次审批")
                            else:
                                return Response("error")
                else:
                    return Response("error")
            else:
                return Response("error")


# 接收表管理
class showrepair_accept(APIView):
    #permission_classes = [permissions.ViewAcceptPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            datas = models.Repair_Manage.objects.filter(orderid__contains="RA").values("orderid", "type", "status")
            for data in datas:
                if data["orderid"].startswith('RA'):
                    info = models.Repair_Accept.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                else:
                    Response("wrong orderid")
            seri = serializer.info_serializer(instance=datas, many=True)
            return Response(seri.data)
        # 有code参数
        else:
            if "orderid" in params.keys():
                orderid = params['orderid']
                datas = models.Repair_Manage.objects.filter(orderid__contains="RA").filter(
                    orderid__contains=orderid).values("orderid", "type", "status")
                for data in datas:
                    if data["orderid"].startswith('RA'):
                        info = models.Repair_Accept.objects.filter(orderid=data["orderid"]).values("info").first()
                        data["info"] = info
                    else:
                        Response("wrong orderid")
                seri = serializer.info_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def delete(self, req):
        reqlist = req.query_params
        orderid = reqlist['orderid']
        row = models.Repair_Accept.objects.filter(orderid=orderid)
        if row.count() == 0:
            return Response('没有找到要删除的订单')
        row2 = models.Repair_Manage.objects.filter(orderid=orderid)
        if row2.count() == 0:
            return Response('没有找到要删除的订单')
        row2.delete()
        row.delete()
        return Response('删除成功')


class addrepair_accept(APIView):
    #permission_classes = [permissions.AddAcceptPermission]
    def get(self, req):
        data = {}
        data["orderid"] = tools.neworderid.getnextRA()
        data["code"] = ""
        data["name"] = ""
        data["type"] = "验收申请单"
        data["info"] = ""
        data["date"] = tools.fortime.nowdatetime()
        seri = serializer.repair_accept_detail_serializer(instance=data)
        return Response(seri.data)

    def post(self, req):
        # url中method参数表示提交或者保存
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "method" in params.keys():
                seri = serializer.repair_accept_detail_serializer(data=req.data)
                if seri.is_valid():
                    equip = models.Equipment.objects.filter(code=seri.validated_data["code"])
                    if equip.count() == 0:
                        return Response("没有对应设备")
                    else:
                        managedata = {}
                        managedata["orderid"] = seri.validated_data["orderid"]
                        managedata["type"] = "维修验收单"
                        if params['method'] == "save":
                            managedata["status"] = "0"
                        else:
                            if params['method'] == "submit":
                                managedata["status"] = "4"
                            else:
                                return Response("error")
                        managedata["maker"] =req.auth.user ##待修改
                        managedata["approver1"] = None
                        managedata["date1"] = tools.fortime.defaulttime()
                        managedata["approver2"] = None
                        managedata["date2"] = tools.fortime.defaulttime()
                        managedata["acceptor"] = None
                        managedata["memo"] = ""
                        #manageseri = serializer.repair_manage_serializer(instance=managedata)
                        models.Repair_Accept.objects.create(**seri.validated_data)
                        #models.Repair_Manage.objects.create(**manageseri.data)
                        models.Repair_Manage.objects.create(**managedata)
                        models.Order_Ids.objects.all().update(RA=tools.neworderid.getnum(seri.validated_data["orderid"]))
                        return Response('添加成功')
                else:
                    return Response(seri.errors)
            else:
                return Response("error")


class showrepair_acceptdetail(APIView):
    #permission_classes = [permissions.ViewAcceptDetailPermission]
    def get(self, req):
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                orderid = params["orderid"]
                datas = models.Repair_Accept.objects.filter(orderid=orderid)
                seri = serializer.repair_accept_detail_serializer(instance=datas, many=True)
                return Response(seri.data)
            else:
                return Response("error")

    def put(self, req):
        # 需要method与orderid参数
        params = req.query_params
        if params == {}:
            return Response("error")
        else:
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    datas = models.Repair_Accept.objects.filter(orderid=orderid)
                    if datas.count() == 0:
                        return Response('没有对应订单')
                    else:
                        seri = serializer.repair_accept_detail_serializer(data=req.data)
                        if seri.is_valid():
                            code = seri.validated_data['code']
                            if models.Equipment.objects.filter(code=code).count() == 0:
                                return Response('没有对应设备')
                            else:
                                if method == "save":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=0, approver1=None,
                                                                                                approver2=None)
                                elif method == "submit":
                                    datas.update(**seri.validated_data)
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(status=4, approver1=None,
                                                                                                approver2=None)
                                else:
                                    return Response("error")
                                return Response("修改成功")
                        else:
                            return Response(seri.errors)
                else:
                    return Response("error")
            else:
                return Response("error")

    def post(self, req):
        # url中method参数确定是提交还是驳回
        params = req.query_params
        data = req.data
        if "memo" not in data.keys():
            return Response("请求体需要且仅需要给出memo")
        else:
            memo = data["memo"]
            if "orderid" in params.keys():
                if "method" in params.keys():
                    orderid = params["orderid"]
                    method = params["method"]
                    if models.Repair_Manage.objects.filter(orderid=orderid).count() == 0:
                        return Response('没有对应订单')
                    else:
                        if method == "reject":
                            models.Repair_Manage.objects.filter(orderid=orderid).update(status=3, approver1=None,
                                                                                        approver2=None, memo=memo)
                            return Response("退回成功")
                        else:
                            if method == "accept":
                                approvers = models.Repair_Manage.objects.filter(orderid=orderid).values("approver1",
                                                                                                        "approver2")[0]
                                if approvers["approver1"] is None:
                                    models.Repair_Manage.objects.filter(orderid=orderid).update(approver1=req.auth.user)  ##待修改
                                    return Response("审批成功")
                                else:
                                    if approvers["approver2"] is None:
                                        models.Repair_Manage.objects.filter(orderid=orderid).update(approver2=req.auth.user,
                                                                                                    status=5)  ##待修改
                                        return Response("审批成功")
                                    else:
                                        return Response("该订单已被审批通过，无需再次审批")
                            else:
                                return Response("error")
                else:
                    return Response("error")
            else:
                return Response("error")


# 所有表展示
class showrepair_manage(APIView):
    #permission_classes = [permissions.ViewManagePermission]
    def get(self, req):
        # 无参
        params = req.query_params
        if 'orderid' not in params.keys():
            datas = models.Repair_Manage.objects.values("orderid", "type", "status")
            for data in datas:
                if data["orderid"].startswith('RP'):
                    info = models.Repair_Schedule.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                elif data["orderid"].startswith('RR'):
                    info = models.Repair_Request.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                elif data["orderid"].startswith('OFF'):
                    info = models.Repair_Off_Req.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                elif data["orderid"].startswith('RA'):
                    info = models.Repair_Accept.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                else:
                    Response("wrong orderid")
            seri = serializer.info_serializer(instance=datas, many=True)
            return Response(seri.data)
        # 有code参数
        else:
            orderid = params['orderid']
            datas = models.Repair_Manage.objects.filter(orderid__contains=orderid).values("orderid", "type", "status")
            for data in datas:
                if data["orderid"].startswith('RP'):
                    info = models.Repair_Schedule.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                elif data["orderid"].startswith('RR'):
                    info = models.Repair_Request.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                elif data["orderid"].startswith('OFF'):
                    info = models.Repair_Off_Req.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                elif data["orderid"].startswith('RA'):
                    info = models.Repair_Accept.objects.filter(orderid=data["orderid"]).values("info").first()
                    data["info"] = info
                else:
                    Response("wrong orderid")
            seri = serializer.info_serializer(instance=datas, many=True)
            return Response(seri.data)
