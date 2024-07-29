from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.user == request.user
