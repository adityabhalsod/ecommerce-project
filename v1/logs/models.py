from email.policy import default
from django.contrib.gis.db import models
from base.models import BaseModel

# Create your models here.
class Log(BaseModel):
    endpoint = models.TextField(default="")  # The url the user requested
    user_agent = models.CharField(default="", max_length=255, null=True, blank=True)
    http_code = models.PositiveSmallIntegerField(default=0)  # Response status code
    http_method = models.CharField(max_length=10, null=True)  # Request method
    user_token = models.TextField(default="")  # user token
    remote_address = models.CharField(max_length=20, null=True)  # IP address of user
    latency_time = models.IntegerField(default=0)  # Time taken to create the response
    traceback = models.TextField(default="")  # traceback
    body_request = models.TextField(default="")  # Request data
    body_response = models.TextField(default="")  # Response data
    body_response_size = models.IntegerField(default=0)  # Response data size

    def __str__(self):
        return "{}:{}:{}:{}".format(
            str(self.http_code),
            str(self.http_method),
            str(self.endpoint),
            str(self.latency_time),
        )
