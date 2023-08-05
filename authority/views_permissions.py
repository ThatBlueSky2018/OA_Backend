from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Roles
from .serializers import PermissionSerializer


class PermissionListView(GenericAPIView, ListModelMixin):
    """
    查看权限列表
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        return self.list(request)


class RoleToPermissionView(APIView):
    """
    角色绑定权限
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        role_id = request.data.get('role_id', [])
        role = Roles.objects.get(pk=role_id)

        permission_ids = request.data.get('permission_ids', [])
        try:
            for permission_id in permission_ids:
                permission = Permission.objects.get(pk=permission_id)
                role.permissions.add(permission)
        except Permission.DoesNotExist:
            return Response({'error': '该权限类型不存在!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '操作成功!'}, status=status.HTTP_200_OK)
