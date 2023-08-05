from django.urls import path, re_path

from .views_user import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserChangePasswordView
from .views_user import UserActivationView, UserDeactivateView, AdminPasswdChangeView

from .views_structure import StructureView, StructureToUserView

urlpatterns = [
    # 用户相关操作
    path("user/list/", UserListView.as_view(), name="user-list"),
    path("user/create/", UserCreateView.as_view(), name="user-create"),
    re_path("^user/detail/(?P<pk>\\d+)", UserDetailView.as_view(), name="user-detail"),
    re_path("^user/update/(?P<pk>\\d+)", UserUpdateView.as_view(), name="user-update"),
    re_path("^user/delete/(?P<pk>\\d+)", UserDeleteView.as_view(), name="user-delete"),
    re_path("^user/changepassword/(?P<pk>\\d+)", UserChangePasswordView.as_view(), name="user_changePassword"),
    re_path("^user/adminpasswdchange/(?P<pk>\\d+)", AdminPasswdChangeView.as_view(), name="user-adminPasswdChange"),
    path('user/activation/', UserActivationView.as_view({'patch': 'batch_activate'}), name='batch-activate'),
    path('user/deactivation/', UserDeactivateView.as_view({'patch': 'batch_deactivate'}), name='batch-deactivate'),

    # 组织架构相关操作
    path("structure/", StructureView.as_view({
        "get": "list",
        "post": "create",
        "patch": "batch_delete"
    })),
    re_path("^structure/(?P<pk>\\d+)$", StructureView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),
    path("structure/add_user/", StructureToUserView.as_view(), name="structure-add_user")
]
