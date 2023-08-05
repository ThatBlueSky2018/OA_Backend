from rest_framework import serializers
from .models import Equipment
from .models import Equ_States
from .models import Repair_Accept
from .models import Repair_Schedule
from .models import Repair_Request
from .models import Repair_Off_Req
from .models import Repair_Manage


class equip_serializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("code", "name", "type", "manufacture", "info", "picture")


class equip_states_serializer(serializers.ModelSerializer):
    class Meta:
        model = Equ_States
        fields = ("code", "purchaser", "use_dep", "life_limit", "time_touse", "status")


class info_serializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    orderid = serializers.CharField()
    type = serializers.CharField()
    info = serializers.CharField()
    status = serializers.CharField()


class repair_schedule_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Schedule
        fields = ("orderid", "type", "info")


class repair_schedule_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Schedule
        fields = ("orderid", "code", "name", "type", "info", "start", "end", "cost", "date")


class repair_request_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Request
        fields = ("orderid", "type", "info")


class repair_request_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Request
        fields = ("orderid", "code", "name", "type", "erro", "info", "start", "end", "cost", "date")


class repair_off_req_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Off_Req
        fields = ("orderid", "type", "info")


class repair_off_req_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Off_Req
        fields = ("orderid", "code", "name", "type", "info", "start", "end", "date")


class repair_accept_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Accept
        fields = ("orderid", "type", "info")


class repair_accept_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Accept
        fields = ("orderid", "code", "name", "type", "info", "date")


class repair_manage_serializer(serializers.ModelSerializer):
    class Meta:
        model = Repair_Manage
        fields = ("orderid", "type", "status", "maker", "approver1", "date1", "approver2", "date2", "acceptor", "memo")
