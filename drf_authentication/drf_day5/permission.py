from rest_framework.permissions import BasePermission

from drf_day5.models import User


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method.lower() in ('get', 'head', 'options'):
            return True
        username = request.data.get("username")
        user = User.objects.filter(username=username).first()
        if user:
            return True
        return False