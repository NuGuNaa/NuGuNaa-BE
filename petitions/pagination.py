from rest_framework.pagination import PageNumberPagination


class CustomResultsSetPagination(PageNumberPagination):
    page_size = 10 # 한 화면에 10개까지만 보여주기
    page_size_query_param = 'page_size'