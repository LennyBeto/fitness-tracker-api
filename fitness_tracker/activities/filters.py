import django_filters
from .models import Activity


class ActivityFilter(django_filters.FilterSet):
    """
    Filter class for Activity model with custom filters
    """
    # Date range filters
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    # Duration range filters
    min_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    max_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    
    # Distance range filters
    min_distance = django_filters.NumberFilter(field_name='distance', lookup_expr='gte')
    max_distance = django_filters.NumberFilter(field_name='distance', lookup_expr='lte')
    
    # Calories range filters
    min_calories = django_filters.NumberFilter(field_name='calories_burned', lookup_expr='gte')
    max_calories = django_filters.NumberFilter(field_name='calories_burned', lookup_expr='lte')
    
    # Text search
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Activity
        fields = {
            'activity_type': ['exact', 'in'],
            'intensity': ['exact', 'in'],
            'date': ['exact', 'year', 'month'],
        }
    
    def filter_search(self, queryset, name, value):
        """
        Custom search filter for title, description, and location
        """
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(location__icontains=value)
        )