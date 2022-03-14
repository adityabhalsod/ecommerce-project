import json
import logging
import threading
import time
import traceback

from account.ip import get_client_ip
from constance import config
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from v1.logs.models import Log

from .helper import set_response

_thread_locals = threading.local()


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.error = ""

    def __call__(self, request):
        response = self.get_response(request)

        response[
            "Access-Control-Allow-Origin"
        ] = "*"  # Allow-origin for access control in headers

        data = (
            {"data": str(self.error)} if config.INTERNAL_SERVER_TRACEBACK_ERROR else {}
        )
        if response.status_code == 500:
            response = set_response(
                "Internal server error",
                False,
                500,
                data,
            )
            return JsonResponse(response, status=response["http_code"])

        if response.status_code == 404 and "<h1>Not Found</h1>" in str(
            response.content
        ):
            logging.error(response.content)
            response = set_response("Page not found", False, response.status_code, {})
            return JsonResponse(response, status=response["http_code"])
        return response

    def process_exception(self, request, exception):
        """
        All logging of internal server error HTTP 500
        """
        self.error = traceback.format_exc()
        logging.error("ERROR")
        logging.error(traceback.format_exc())
        response = set_response("Internal server error", False, 500, {})
        return JsonResponse(response, status=response["http_code"])


class LoggingMiddleware(MiddlewareMixin):
    """
    Provides full logging of requests and responses
    """

    initial_http_body = None
    _time = None

    def process_request(self, request):
        self._time = time.time()
        _thread_locals.request = request
        self.initial_http_body = request.body

    def process_response(self, request, response):
        """
        Adding request and response logging
        """
        ip_address, routable = get_client_ip(request)
        user_agent = str(request.META.get("HTTP_USER_AGENT", ""))[:255]

        if "api/v1" in str(request.get_full_path()) or "robots.txt" in str(
            request.get_full_path()
        ):
            self._time = int((time.time() - self._time) * 1000)
            try:
                request_data = {
                    "endpoint": str(request.get_full_path()),
                    "user_agent": str(user_agent),
                    "http_code": response.status_code,
                    "http_method": str(request.method),
                    "remote_address": str(ip_address),
                    "latency_time": str(self._time),
                    "traceback": str(traceback.format_exc()),
                    "body_request": str(self.initial_http_body.decode("utf-8"))
                    if self.initial_http_body
                    else "",
                    "body_response": str(response.content.decode("utf-8")),
                    "body_response_size": len(response.content),
                }
                Log.objects.create(**request_data)
            except Exception:
                print(traceback.format_exc())

        return response
