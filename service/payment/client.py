from __future__ import print_function
from constance import config

import requests


class PaymentClient(object):
    """
    Client for cashfree payment getway.
    """

    def __init__(self):
        if config.IS_ACTIVE_LIVE_ENVIRONMENT:
            URL = "https://api.cashfree.com/"
            ID = config.PAYMENT_APP_ID_LIVE
            SECRET_KEY = config.PAYMENT_SECRET_KEY_LIVE
        else:
            URL = "https://test.cashfree.com/"
            ID = config.PAYMENT_APP_ID_TEST
            SECRET_KEY = config.PAYMENT_SECRET_KEY_TEST

        self.url = URL

        self.headers = {
            "Accept": "application/json",
            "x-client-id": ID,
            "x-client-secret": SECRET_KEY,
            "Content-Type": "application/json",
            "x-api-version": "2022-01-01",
        }

        self.kwargs = {}
        self.params = {}

    def create_order(self, kwargs):
        self.url = self.url + "api/v2/cftoken/order"
        self.kwargs = kwargs
        return self.post()

    def payment_by_id(self):
        raise NotImplemented

    def refunds(self):
        raise NotImplemented

    def create_refund(self):
        raise NotImplemented

    def get_all_refunds_for_an_order(self):
        raise NotImplemented

    def get_refund(self):
        raise NotImplemented

    def settlements(self):
        raise NotImplemented

    def create_payment_link(self, kwargs):
        self.url = self.url + "/links"
        self.kwargs = kwargs
        return self.post()

    def fetch_payment_link_details(self):
        raise NotImplemented

    def create_payment(self):
        raise NotImplemented

    def create_qr_code(self):
        raise NotImplemented

    def balance(self):
        raise NotImplemented

    def self_withdrawal(self):
        raise NotImplemented

    def internal_transfer(self):
        raise NotImplemented

    def payout(self):
        raise NotImplemented

    def verify_aadhar_card(self):
        raise NotImplemented

    def verify_pan_card(self):
        raise NotImplemented

    def verify_bank_account(self):
        raise NotImplemented

    def verify_upi_account(self):
        raise NotImplemented

    def verify_ifsc_code(self):
        raise NotImplemented

    def add_beneficiary(self):
        raise NotImplemented

    def get_beneficiary_details(self):
        raise NotImplemented

    def beneficiary_id(self):
        raise NotImplemented

    def remove_beneficiary(self):
        raise NotImplemented

    def beneficiary_history(self):
        raise NotImplemented

    def post(self):
        print("Post request for payment getway URL :::: ", self.url)
        print("Post request for payment getway DATA :::: ", self.kwargs)
        response = requests.post(
            self.url,
            json=self.kwargs,
            headers=self.headers,
        )
        if response.status_code != 200:
            print("Error on post method")
        return response.json()

    def get(self):
        print("GET request for payment getway URL :::: ", self.url)
        print("GET request for payment getway DATA :::: ", self.kwargs)
        response = requests.get(
            self.url,
            params=self.params,
            headers=self.headers,
        )
        if response.status_code != 200:
            print("Error on get method")
        return response.json()
