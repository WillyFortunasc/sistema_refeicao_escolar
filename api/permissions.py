from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Somente papel 'admin'."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel == "admin"
        )


class IsFiscal(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel == "fiscal"
        )


class IsGestor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel == "gestor"
        )


class IsEmpresa(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel == "empresa"
        )


class IsOperador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel == "operador"
        )


class IsAdminOrGestor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel in ("admin", "gestor")
        )
