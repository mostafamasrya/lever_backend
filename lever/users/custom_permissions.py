from rest_framework import permissions


# class AllowAllUsers(permissions.BasePermission):
#     """
#     Allows access to all users, (instructor, assistant, student)
#     """

#     def has_permission(self, request, view):
#         return not request.user.date_deleted and (request.user.type == "player" or request.user.type == "owner")
    

# class IsOwner(permissions.BasePermission):
#     """
#     Allows access only to users classified as `Owner`.
#     """

#     def has_permission(self, request, view):
#         return not request.user.date_deleted and (request.user.type == "owner" and not request.user.date_deleted and request.user.is_active)


# class IsPlayer(permissions.BasePermission):
#     """
#     Allows access only to users classified as `Player`.
#     """

#     def has_permission(self, request, view):
#         return not request.user.date_deleted and (request.user.type == "player" and not request.user.date_deleted and request.user.is_active)

