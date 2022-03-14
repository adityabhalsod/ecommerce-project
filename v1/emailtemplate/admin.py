from django.contrib import admin

from base.admin import BaseAdmin
from v1.emailtemplate.models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(BaseAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
