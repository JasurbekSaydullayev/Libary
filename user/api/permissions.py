from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser
