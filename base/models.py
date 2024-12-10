from django.contrib.gis.db import models
from django.utils import timezone


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['-id']

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def get_app_label(self):
        return self.__class__._meta.app_label  # Returns the app label dynamically

    def archive(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()
