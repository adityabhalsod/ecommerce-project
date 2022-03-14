from .country_code import CountryCode
from .exceptions import InvalidCountryCode


def prefix_country_code(country_code, number):
    """Prefix country code to phone number
    Args:
        country_code: the country code to prefix of type CountryCode
        number (str): the mobile number
    Raises:
        InvalidCountryCode when supplied country code is not type of CountryCode
    Returns:
        number (str): mobile number with country code prefixed. if country_code
        is already prefixed, then the same is returned unaltered.
    """
    if not isinstance(country_code, CountryCode):
        raise InvalidCountryCode("The country code should be of type CountryCode")
    if len(number) == 10 and (not number.startswith(country_code.value)):
        number = country_code.value + number
    return number
