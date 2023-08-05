from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Structure, UserProfile
from .serializers import StructureSerializer


# Create your views here.
class StructureView(ModelViewSet):
    """
    组织架构视图
    """
    queryset = Structure.objects.all()
    permission_classes = [IsAdminUser]  # 只有管理员才能管理组织架构的增删改查
    serializer_class = StructureSerializer

    @action(methods=['patch'], detail=False)
    def batch_delete(self, request):
        # 获取要删除的组织架构的ID列表
        structure_ids = request.data.get('structure_ids', None)

        if structure_ids is not None:
            # 删除指定ID的组织架构
            deleted_count, _ = Structure.objects.filter(id__in=structure_ids).delete()

            if deleted_count > 0:
                return Response({'detail': '批量删除成功'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': '未找到指定的组织架构'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': '未提供有效的组织架构ID列表'}, status=status.HTTP_400_BAD_REQUEST)


class StructureToUserView(APIView):
    """
    用户关联部门
    """
    permission_classes = [IsAdminUser]  # 只有管理员才能将用户与部门关联

    def put(self, request):
        structure_id = request.data.get('structure_id')
        user_ids = request.data.get('user_ids', [])

        structure = get_object_or_404(Structure, id=structure_id)
        users = UserProfile.objects.filter(id__in=user_ids)

        for user in users:
            user.department = structure
            user.save()

        return Response({'detail': "修改成功"}, status=status.HTTP_200_OK)
