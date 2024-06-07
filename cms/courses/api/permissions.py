from rest_framework.permissions import BasePermission

from courses.models import Course


class IsEnrolled(BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        if not isinstance(obj, Course):
            return False

        return obj.students.filter(id=request.user.id).exists()
