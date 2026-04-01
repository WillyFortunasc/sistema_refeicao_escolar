from rest_framework.permissions import BasePermission

class IsFiscal(BasePermission):
    def has_permission(self, request, view):
        return request.user.papel == "fiscal"

class IsGestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.papel == "gestor"

class IsEmpresa(BasePermission):
    def has_permission(self, request, view):
        return request.user.papel == "empresa"
