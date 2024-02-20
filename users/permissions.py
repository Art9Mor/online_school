from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    message = 'You are not in a moderator group'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj=None):
#         return obj.owner == request.user

class IsOwner(BasePermission):
    message = 'You are not an owner of this'

    def has_object_permission(self, request, view, obj=None):
        if obj.owner == request.user:
            return request.method in ('GET', 'PUT', 'PATCH', 'DELETE')
        return False