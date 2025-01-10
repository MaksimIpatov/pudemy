from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    """Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.groups.filter(name="moderator").exists()
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(BasePermission):
    """Разрешает доступ модераторам или владельцам объекта."""

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or request.user.groups.filter(name="moderator").exists()
        )

    def has_permission(self, request, view):
        return (
            request.user.groups.filter(name="moderator").exists()
            or request.method in SAFE_METHODS
        )
