from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityDetailView,
    activity_metrics,
    activity_type_stats,
    recent_activities
)

app_name = 'activities'

urlpatterns = [
    # Activity CRUD endpoints
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    
    # Metrics and statistics endpoints
    path('metrics/', activity_metrics, name='activity-metrics'),
    path('type-stats/', activity_type_stats, name='activity-type-stats'),
    path('recent/', recent_activities, name='recent-activities'),
]