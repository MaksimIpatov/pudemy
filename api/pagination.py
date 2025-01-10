from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = settings.PAGE_SIZE
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_PAGE_SIZE


class CoursePagination(PageNumberPagination):
    page_size = settings.COURSE_PAGE_SIZE
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_PAGE_SIZE


class LessonPagination(PageNumberPagination):
    page_size = settings.LESSON_PAGE_SIZE
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_PAGE_SIZE
