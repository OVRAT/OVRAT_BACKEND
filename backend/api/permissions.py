from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
    """
    Permettre aux utilisateurs ayant un certain rôle de modifier un attribut spécifique d'un modèle.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser == True:
            # Autoriser les utilisateurs ayant le rôle 'super user'
            return True
        return False

    # def has_object_permission(self, request, view, obj):
    #     # Autoriser les requêtes GET, HEAD ou OPTIONS
    #     if request.method in ['GET', 'HEAD', 'OPTIONS']:
    #         return True
    #     return False



