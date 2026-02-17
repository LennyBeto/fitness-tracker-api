from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Avg, Count, Q, Max, Min
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Activity
from .serializers import (
    ActivitySerializer,
    ActivityCreateSerializer,
    ActivitySummarySerializer,
    ActivityTypeStatsSerializer
)
from .filters import ActivityFilter


class ActivityPagination(PageNumberPagination):
    """
    Custom pagination for activities
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ActivityListCreateView(generics.ListCreateAPIView):
    """
    List all activities or create a new activity
    GET /api/activities/ - List all activities (with filtering, sorting, pagination)
    POST /api/activities/ - Create new activity
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ActivityPagination
    filterset_class = ActivityFilter
    ordering_fields = ['date', 'duration', 'distance', 'calories_burned', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        """
        Return activities for the current user only
        """
        return Activity.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ActivityCreateSerializer
        return ActivitySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an activity
    GET /api/activities/{id}/ - Get activity details
    PUT/PATCH /api/activities/{id}/ - Update activity
    DELETE /api/activities/{id}/ - Delete activity
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Ensure users can only access their own activities
        """
        return Activity.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ActivityCreateSerializer
        return ActivitySerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_metrics(request):
    """
    Get activity metrics and summary for the current user
    GET /api/activities/metrics/
    
    Query parameters:
    - date_from: Start date (YYYY-MM-DD)
    - date_to: End date (YYYY-MM-DD)
    - activity_type: Filter by activity type
    - period: Predefined periods (week, month, year)
    """
    user = request.user
    
    # Get query parameters
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    activity_type = request.query_params.get('activity_type')
    period = request.query_params.get('period')
    
    # Build base queryset
    queryset = Activity.objects.filter(user=user)
    
    # Apply date filters
    if period:
        today = timezone.now().date()
        if period == 'week':
            date_from = today - timedelta(days=7)
        elif period == 'month':
            date_from = today - timedelta(days=30)
        elif period == 'year':
            date_from = today - timedelta(days=365)
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if activity_type:
        queryset = queryset.filter(activity_type=activity_type)
    
    # Calculate summary statistics
    stats = queryset.aggregate(
        total_activities=Count('id'),
        total_duration=Sum('duration'),
        total_distance=Sum('distance'),
        total_calories=Sum('calories_burned'),
        average_duration=Avg('duration'),
        average_distance=Avg('distance'),
        average_calories=Avg('calories_burned'),
    )
    
    # Get activity breakdown by type
    activity_breakdown = queryset.values('activity_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    breakdown_dict = {
        item['activity_type']: item['count'] 
        for item in activity_breakdown
    }
    
    # Find most common activity
    most_common = activity_breakdown.first()
    most_common_activity = most_common['activity_type'] if most_common else None
    
    # Prepare response data
    summary_data = {
        'total_activities': stats['total_activities'] or 0,
        'total_duration': stats['total_duration'] or 0,
        'total_distance': stats['total_distance'] or Decimal('0.00'),
        'total_calories': stats['total_calories'] or 0,
        'average_duration': round(stats['average_duration'] or 0, 2),
        'average_distance': round(stats['average_distance'] or 0, 2),
        'average_calories': round(stats['average_calories'] or 0, 2),
        'most_common_activity': most_common_activity,
        'activity_breakdown': breakdown_dict,
    }
    
    serializer = ActivitySummarySerializer(summary_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_type_stats(request):
    """
    Get detailed statistics for each activity type
    GET /api/activities/type-stats/
    """
    user = request.user
    
    # Get query parameters
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    
    # Build base queryset
    queryset = Activity.objects.filter(user=user)
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    # Get stats by activity type
    type_stats = queryset.values('activity_type').annotate(
        count=Count('id'),
        total_duration=Sum('duration'),
        total_distance=Sum('distance'),
        total_calories=Sum('calories_burned'),
        average_duration=Avg('duration'),
        average_distance=Avg('distance'),
        average_calories=Avg('calories_burned'),
    ).order_by('-count')
    
    # Format the data
    stats_list = []
    for stat in type_stats:
        stats_list.append({
            'activity_type': stat['activity_type'],
            'count': stat['count'],
            'total_duration': stat['total_duration'] or 0,
            'total_distance': round(stat['total_distance'] or 0, 2),
            'total_calories': stat['total_calories'] or 0,
            'average_duration': round(stat['average_duration'] or 0, 2),
            'average_distance': round(stat['average_distance'] or 0, 2),
            'average_calories': round(stat['average_calories'] or 0, 2),
        })
    
    serializer = ActivityTypeStatsSerializer(stats_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recent_activities(request):
    """
    Get recent activities (last 10)
    GET /api/activities/recent/
    """
    user = request.user
    activities = Activity.objects.filter(user=user).order_by('-date', '-created_at')[:10]
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)