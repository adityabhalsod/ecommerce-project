"""
Django rest framework default pagination
"""
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 10
    page_query_param = "offset"
    page_size_query_param = "limit"
    max_page_size = 100
