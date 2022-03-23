from requests import Response


def convert_response(response: Response, **kwargs):
    """Convert requests package response obj to our internal Response
    Args:
        response: the response object returned by requests package
        kwargs : any other optional keyword parameters
    Returns:
        our internal ServiceResponse object
    """
    message = ""
    if response.json().get("type") == "error":
        message = response.json().get("message")
        status = "error"
    elif response.json().get("type") == "success":
        message = response.json().get("message")
        status = "success"
    print({status: message})
    return {status: message}
