from django_filters import rest_framework as drf_filters
from .models import Post


class PostFilter(drf_filters.FilterSet):
    created_year = drf_filters.NumberFilter(field_name='created_time', lookup_expr='year')
    created_month = drf_filters.NumberFilter(field_name='created_time', lookup_expr='month')

    class Meta:
        model = Post
        fields = ['tags', 'category', 'created_year', 'created_month']