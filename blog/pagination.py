from rest_framework.pagination import PageNumberPagination

class BlogPageNumberPagination(PageNumberPagination):
    page_size = 10  # 默认一页显示的条数
    page_query_param = 'page'   # 定义url中获取页码用到的参数
    page_size_query_param = 'page_size' # 调整每页显示数量的参数名
    max_page_size = 20  # 用户最大可自定义一页的条数
