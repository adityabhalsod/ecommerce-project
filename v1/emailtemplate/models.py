from ckeditor.fields import RichTextField
from django.contrib.gis.db import models

from base.models import BaseModel
from v1.emailtemplate.choice import EmailTemplateChoices


# Create your models here.
class EmailTemplate(BaseModel):
    title = models.CharField(
        max_length=255, unique=True, choices=EmailTemplateChoices.choices
    )
    subject = models.CharField(max_length=1024, default="")
    html_content = RichTextField(default="")

    def __str__(self):
        return str(self.title)
