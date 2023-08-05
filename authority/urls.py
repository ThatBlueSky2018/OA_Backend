from django.urls import path, re_path
from .views_menu import MenuView
from .views_role import RoleView, RoleToUserView, RoleToMenuView
from .views_permissions import PermissionListView, RoleToPermissionView

urlpatterns = [
    # 角色相关路由
    path("roles/", RoleView.as_view({
        "get": "list",
        "post": "create",
        "patch": "batch_delete"
    })),
    re_path("^roles/(?P<pk>\\d+)$", RoleView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),

    path("roles/user_role/", RoleToUserView.as_view(), name="userprofile_roles"),
    path("roles/roles_permission/", RoleToMenuView.as_view(), name="roles_permission"),

    # 菜单相关路由
    path("menu/", MenuView.as_view({
        "get": "list",
        "post": "create",
        "patch": "batch_delete"
    })),
    re_path("^menu/(?P<pk>\\d+)$", MenuView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),

    path("permissions/", PermissionListView.as_view(), name="permission_list"),
    path("role_permissions/", RoleToPermissionView.as_view(), name="role_to_permission")
]
