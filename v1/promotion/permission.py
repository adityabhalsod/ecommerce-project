from base.permission import ModelPermission


class ReferralAndEarnPermission(ModelPermission):
    def has_permission(self, request, view):
        if view.action == "earning_price":
            return True
