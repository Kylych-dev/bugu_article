from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        # Проверка для crud
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and hasattr(request.user, 'author_profile')
        return True
    
    def has_object_permission(self, request, view, obj):
        # Проверка на автора статьи
        return obj.author == request.user
    
