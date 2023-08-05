########################################
from rest_framework.permissions import BasePermission


class ViewEquipPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view 设备信息':
                    return True
        return False


#
class AddEquipPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can add 设备信息':
                    return True
        return False


#
class ViewStatePermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view state':
                    return True
        return False


#
class AddStatePermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can add state':
                    return True
        return False


#
class ViewSchedulePermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view schedule':
                    return True
        return False


#
class AddSchedulePermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can add schedule':
                    return True
        return False


#
class ViewscheduleDetailPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view scheduledetail':
                    return True
        return False


#
class ViewRequestPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view request':
                    return True
        return False


#
class AddRequestPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can add request':
                    return True
        return False


#
class ViewRequestDetailPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view requestdetail':
                    return True
        return False


#
class ViewOffPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view off':
                    return True
        return False


#
class AddOffPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can add off':
                    return True
        return False


#
class ViewOffDetailPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view offdetail':
                    return True
        return False


#
class ViewAcceptPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view accept':
                    return True
        return False


#
class AddAcceptPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can add accept':
                    return True
        return False


#
class ViewAcceptDetailPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view acceptdetail':
                    return True
        return False


class ViewManagePermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user = token.user
        for role in user.role.all():
            for permission in role.permissions.all():
                if permission.name == 'Can view manage':
                    return True
        return False
