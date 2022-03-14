import requests

from ..utils.country_code import CountryCode
from ..utils.mobile_number import prefix_country_code
from .utils import convert_response


class BaseClient:
    """Base class for both OTPClient"""

    base_url = "https://api.msg91.com"
    otp_endpoint = "/api/v5/otp"
    otp_retry_endpoint = "/api/v5/otp/retry"
    verify_otp_endpoint = "/api/v5/otp/verify"

    def __init__(self, auth_key):
        self.auth_key = auth_key

    def get_otp_url(self):
        return self.base_url + self.otp_endpoint

    def get_resend_otp_url(self):
        return self.base_url + self.otp_retry_endpoint

    def get_verify_otp_url(self):
        return self.base_url + self.verify_otp_endpoint

    def get_otp_payload(self, mobile_number, **kwargs):
        mobile_number = prefix_country_code(CountryCode.INDIA, str(mobile_number))
        return {"mobile": mobile_number, "authkey": self.auth_key, **kwargs}

    def get_resend_otp_payload(self, mobile_number, retry_type, **kwargs):
        mobile_number = prefix_country_code(CountryCode.INDIA, str(mobile_number))
        payload = {
            "mobile": mobile_number,
            "authkey": self.auth_key,
            "retrytype": retry_type,
            **kwargs,
        }
        return payload

    def get_verify_payload_headers(self, mobile_number, otp_value, **kwargs):
        mobile_number = prefix_country_code(CountryCode.INDIA, str(mobile_number))
        payload = {
            "authkey": self.auth_key,
            "mobile": mobile_number,
            "otp": otp_value,
            **kwargs,
        }
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        return (payload, headers)


class OTPClient(BaseClient):
    """Synchronous OTP client
    Use this class for blocking request to API
    """

    def send_otp(self, mobile_number, **kwargs):
        """Request the Service to send OTP message to given number
        Args:
            mobile_number(str): 10 digit mobile number with country code of receiver

            message(str, optional): text message to send along with OTP
            sender(str, optional): the name to appear in SMS as sender
            otp (int, optional): the opt value to send, if not service will generate
            otp_length (int, optional): the length of otp. default 4, max 9
        Returns:
            a response object with status and status message
        """
        otp_url = self.get_otp_url()
        payload = self.get_otp_payload(mobile_number, **kwargs)
        service_response = requests.get(otp_url, params=payload)
        _response = convert_response(service_response, identifier=mobile_number)
        return _response

    def resend_otp(self, mobile_number, retry_type, **kwargs):
        """Resend OTP request
        Args:
            mobile_number(str): 10 digit mobile number with country code of mobile_number
        Returns:
            a response object with status and status message
        """
        retry_url = self.get_resend_otp_url()
        payload = self.get_resend_otp_payload(mobile_number, retry_type, **kwargs)
        service_response = requests.get(retry_url, params=payload)
        _response = convert_response(service_response)
        return _response

    def verify_otp(self, mobile_number, otp_value, **kwargs):
        """Request to verify OTP with given mobile_number number
        Args:
            mobile_number(str): mobile number to verify otp
            otp_value(int): the otp value to verify against
        Returns:
             a response object with status and status message
        """
        verify_url = self.get_verify_otp_url()
        payload, headers = self.get_verify_payload_headers(
            mobile_number, otp_value, **kwargs
        )
        service_response = requests.get(verify_url, params=payload, headers=headers)
        _response = convert_response(service_response)
        return _response
