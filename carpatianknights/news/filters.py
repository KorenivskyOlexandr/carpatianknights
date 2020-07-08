import django_filters


class PostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name='publish', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='publish', lookup_expr='lte')
