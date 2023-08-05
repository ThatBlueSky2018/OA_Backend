from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Menu
from .serializers import MenuSerializer


# Create your views here.
class MenuView(ModelViewSet):
    """
    菜单视图，管理菜单的增删改查
    """
    permission_classes = [IsAdminUser]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(methods=['patch'], detail=False)
    def batch_delete(self, request):
        # 获取要删除的组织架构的ID列表
        menu_ids = request.data.get('menu_ids', None)

        if menu_ids is not None:
            # 删除指定ID的组织架构
            deleted_count, _ = Menu.objects.filter(id__in=menu_ids).delete()

            if deleted_count > 0:
                return Response({'detail': '批量删除成功'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': '未找到指定的菜单'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': '未提供有效的菜单ID列表'}, status=status.HTTP_400_BAD_REQUEST)
