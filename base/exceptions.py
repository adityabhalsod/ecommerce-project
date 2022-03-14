from rest_framework import status
from rest_framework.views import exception_handler as base_handler


def exception_handler(exception, context):
    """
    Django rest framework for custom exception handler

    @exception  :  Exception
    @context    :  Context
    """
    response = base_handler(exception, context)

    if response is not None:
        response = custom_response(response)

    return response


def serializer_errors(data):
    """
    Django rest framework serializing the errors
    @data  : data is python error dictionary
    """
    errors = {}
    got_msg = False
    message = "Bad request."

    if isinstance(data, dict):
        for key, value in data.items():
            try:
                if isinstance(value, list):
                    value = ", ".join(value)
            except Exception:
                pass

            if not got_msg:
                if value:
                    message = value
                    got_msg = True
            errors[key] = value

    if not isinstance(message, str):
        message = "Bad request"
    return errors, message


def error(source, detail, code):
    """
    Create python dictionary of error
    @source : Where coming the error
    @detail : Error detail information
    """
    error = {}
    error["source"] = source
    error["detail"] = detail
    if code:
        error["code"] = code
    return error


def custom_response(response):
    """
    Modification the response of django rest framework

    @response : Return response
    """
    modified_data = {}
    modified_data["code"] = response.status_code
    modified_data["status"] = get_status(response.status_code)
    data, message = serializer_errors(response.data)
    modified_data["message"] = message
    modified_data["errors"] = data
    response.data = modified_data
    return response


def get_status(status_code):
    """
    Return result base on return http status

    @status_code : HTTP status code
    """
    result = ""

    if status_code == status.HTTP_200_OK:
        result = "Success"
    elif status_code == status.HTTP_201_CREATED:
        result = "Instance create"
    elif status_code == status.HTTP_204_NO_CONTENT:
        result = "Instance deleted"
    elif status_code == status.HTTP_403_FORBIDDEN:
        result = "Forbidden error"
    elif status_code == status.HTTP_404_NOT_FOUND:
        result = "Instance not found"
    elif status_code == status.HTTP_400_BAD_REQUEST:
        result = "Bad request"
    elif status_code == status.HTTP_401_UNAUTHORIZED:
        result = "Unauthorized request"
    elif status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        result = "Internal server error"
    else:
        result = "Unknown error"

    return result
