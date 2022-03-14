from django import forms
from django.contrib.auth.models import Permission
from account.utils import get_projects_apps_models


class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields["permissions"].queryset = Permission.objects.filter(
            content_type__app_label__in=get_projects_apps_models()
        )
