from rest_framework.response import Response as DRFResponse

from base.exceptions import get_status


class Response(DRFResponse):
    def __init__(self, data={}, message="", status=None, *args, **kwargs):
        if not message:
            message = "Bad request."
        modified_data = {}
        modified_data["code"] = status
        modified_data["status"] = get_status(status)
        modified_data["message"] = message
        modified_data["data"] = data

        super(Response, self).__init__(
            data=modified_data, status=status, *args, **kwargs
        )
