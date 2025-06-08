import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='sender__username', lookup_expr='exact')
    after_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    before_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'after_date', 'before_date']
