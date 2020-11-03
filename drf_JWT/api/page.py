from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class MyPageNumberPagination(PageNumberPagination):

    page_size = 2
    max_page_size = 5
    page_size_query_param = "page_size"
    page_query_param = "page"


class MyLimitOffsetPagination(LimitOffsetPagination):

    default_limit = 3
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 5