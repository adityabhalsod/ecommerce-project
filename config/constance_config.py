# A ==> Z
MY_CONSTANCE_CONFIG = {
    ##### Customer
    "CUSTOMER_DEFAULT_MOBILE_NUMBER": (
        "",
        "Customer default mobile number",
        str,
    ),
    "CUSTOMER_DEFAULT_EMAIL_ADDRESS": (
        "",
        "Customer default email ID",
        str,
    ),
    ##### Customer
    #  Google maps
    "GOOGLE_MAPS_API_KEY": (
        "",
        "Google maps api key.",
        str,
    ),
    #  Google maps
    # API Related
    "INTERNAL_SERVER_TRACEBACK_ERROR": (
        False,
        "We can showing traceback in response?",
        bool,
    ),
    # API Related
    #### OTP Related
    "MSG_91_AUTH_KEY": (
        "",
        "Message91 auth key.",
        str,
    ),
    "OTP_EXPIRY_TIME": (
        1,
        "Expiry of OTP to verify, in minutes (default : 1 day, min : 1 minute)",
        int,
    ),
    "OTP_LENGTH": (4, "Number of digits in OTP (default : 4, min : 4, max : 9) ", int),
    #### OTP Related
    ### Mail Related
    "DEFAULT_FROM_EMAIL": (
        "",
        "Sendgrid EMAIL KEY.",
        str,
    ),
    "EMAIL_CONFIRMATION_EXPIRE_DAYS": (
        3,
        "Email confirmation expire days.",
        int,
    ),
    "EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL": (
        "",
        "Email confirmation authenticated redirect url",
        str,
    ),
    "MAX_EMAIL_ADDRESSES": (
        5,
        "User to allowed max email address.",
        int,
    ),
    "SEND_GRID_API_KEY": (
        "",
        "Sendgrid EMAIL KEY.",
        str,
    ),
    ### Mail Related
    ### First order delivery charge
    "FIRST_ORDER_DELIVERY_CHARGE": (
        True,
        "While first order of any customer to first time set delivery charge or not? (IsCheck means charge)",
        bool,
    ),
    ### First order delivery charge
    ### Payment ###
    "IS_ACTIVE_LIVE_ENVIRONMENT": (
        False,
        "Current which environment is working for payment server.",
        bool,
    ),
    "PAYMENT_APP_ID_LIVE": (
        "",
        "Payment APP ID (LIVE).",
        str,
    ),
    "PAYMENT_SECRET_KEY_LIVE": (
        "",
        "Payment secret KEY (LIVE).",
        str,
    ),
    "PAYMENT_APP_ID_TEST": (
        "",
        "Payment APP ID (TEST).",
        str,
    ),
    "PAYMENT_SECRET_KEY_TEST": (
        "",
        "Payment secret KEY (TEST).",
        str,
    ),
    "MAXIMUM_CASE_DELIVERY": (
        0.0,
        "Set maximum amount order for case delivery.",
        float,
    ),
    ### Payment ###
    ### Referral code ###
    "REFER_AND_EARN_PRICE": (
        0.0,
        "In refer and earn code to earning price.",
        float,
    ),
    ### Referral code ###
}
