from rest_framework import generics, permissions
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import APILog
from .serializers import APILogSerializer, APILogSummarySerializer


class APILogFilter(filters.FilterSet):
    """Filter for API logs"""
    method = filters.CharFilter(lookup_expr='iexact')
    path = filters.CharFilter(lookup_expr='icontains')
    response_status_code = filters.NumberFilter()
    request_user = filters.NumberFilter()
    date_from = filters.DateTimeFilter(
        field_name='request_timestamp', lookup_expr='gte'
    )
    date_to = filters.DateTimeFilter(
        field_name='request_timestamp', lookup_expr='lte'
    )
    
    class Meta:
        model = APILog
        fields = [
            'method', 'path', 'response_status_code', 'request_user',
            'date_from', 'date_to'
        ]


class APILogListView(generics.ListAPIView):
    """View to list API logs with filtering"""
    queryset = APILog.objects.all()
    serializer_class = APILogSummarySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = APILogFilter
    ordering = ['-request_timestamp']
    ordering_fields = ['request_timestamp', 'duration_ms', 'response_status_code']


class APILogDetailView(generics.RetrieveAPIView):
    """View to get detailed information about a specific API log"""
    queryset = APILog.objects.all()
    serializer_class = APILogSerializer
    permission_classes = [permissions.IsAdminUser]


class APILogStatsView(generics.GenericAPIView):
    """View to get API usage statistics"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        """Get API usage statistics"""
        from django.db.models import Count, Avg, Min, Max
        from django.utils import timezone
        from datetime import timedelta
        
        # Get date range from query params
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter logs by date range
        logs = APILog.objects.filter(
            request_timestamp__range=(start_date, end_date)
        )
        
        # Calculate statistics
        stats = {
            'total_requests': logs.count(),
            'unique_endpoints': logs.values('path').distinct().count(),
            'unique_users': logs.values('request_user').distinct().count(),
            'avg_response_time': logs.aggregate(
                avg_time=Avg('duration_ms')
            )['avg_time'] or 0,
            'status_code_distribution': logs.values('response_status_code').annotate(
                count=Count('id')
            ).order_by('response_status_code'),
            'method_distribution': logs.values('method').annotate(
                count=Count('id')
            ).order_by('method'),
            'top_endpoints': logs.values('path').annotate(
                count=Count('id')
            ).order_by('-count')[:10],
            'date_range': {
                'start': start_date,
                'end': end_date,
                'days': days
            }
        }
        
        return Response(stats) 