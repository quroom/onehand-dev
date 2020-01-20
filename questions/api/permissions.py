from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsQuestionAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.question.author == request.user

class IsAuthenticatedOrQuestionListOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'list':
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.profile.category!=1:
            return True
        else:
            return obj.author == request.user