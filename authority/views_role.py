from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Roles, Menu
from organization.models import UserProfile
from .serializers import RoleSerializer


class RoleView(ModelViewSet):
    """
    角色视图，管理角色的增删改查
    """
    queryset = Roles.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RoleSerializer

    @action(methods=['patch'], detail=False)
    def batch_delete(self, request):
        # 获取要删除的组织架构的ID列表
        role_ids = request.data.get('role_ids', None)

        if role_ids is not None:
            # 删除指定ID的组织架构
            deleted_count, _ = Roles.objects.filter(id__in=role_ids).delete()

            if deleted_count > 0:
                return Response({'detail': '批量删除成功'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': '未找到指定的角色'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': '未提供有效的角色ID列表'}, status=status.HTTP_400_BAD_REQUEST)


class RoleToUserView(APIView):
    """
    用户关联角色
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        role_id = request.data.get('role_id', [])
        role = Roles.objects.get(pk=role_id)

        # 获取要关联的用户ID列表
        user_ids = request.data.get('user_ids', [])
        for user_id in user_ids:
            try:
                user = UserProfile.objects.get(pk=user_id)
                user.role.add(role)
            except UserProfile.DoesNotExist:
                return Response({'error': '该用户不存在!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '操作成功!'}, status=status.HTTP_200_OK)


class RoleToMenuView(APIView):
    """
    角色绑定菜单
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        role_id = request.data.get('role_id', [])
        role = Roles.objects.get(pk=role_id)

        menu_ids = request.data.get('menu_ids', [])
        try:
            for menu_id in menu_ids:
                menu = Menu.objects.get(pk=menu_id)
                role.permission.add(menu)
        except Menu.DoesNotExist:
            return Response({'error': '该菜单不存在!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '操作成功!'}, status=status.HTTP_200_OK)


