from base.permission import AdminPermission


class AuthenticationPermission(AdminPermission):
    def has_permission(self, request, view):
        if view.action == "password_change":
            if self.has_admin_permission(request):
                return True
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == "password_change":
            if self.has_admin_permission(request):
                return True
            return (
                request.user and request.user.is_authenticated and obj == request.user
            )
        return True


class ProfilePermission(AdminPermission):
    def has_permission(self, request, view):
        if view.action in ["update", "partial_update", "destroy"]:
            if self.has_admin_permission(request):
                return True
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == "password_change":
            if self.has_admin_permission(request):
                return True

            return (
                request.user and request.user.is_authenticated and obj == request.user
            )
        return True


class ProfilePhotoPermission(AdminPermission):
    def has_permission(self, request, view):
        if view.action in ["create", "update", "update", "partial_update", "destroy"]:
            if self.has_admin_permission(request):
                return True
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ["create", "update", "update", "partial_update", "destroy"]:
            if self.has_admin_permission(request):
                return True

            return (
                request.user
                and request.user.is_authenticated
                and obj.user == request.user
            )
        return True


class AddressPermission(AdminPermission):
    def has_permission(self, request, view):
        if view.action:
            if self.has_admin_permission(request):
                return True
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action:
            if self.has_admin_permission(request):
                return True

            if (
                request.user
                and request.user.is_authenticated
                and obj.user
                and obj.user == request.user
            ):
                return True
        return False
