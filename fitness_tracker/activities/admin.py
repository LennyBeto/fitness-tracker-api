from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    Admin configuration for Activity model
    """
    list_display = (
        'title', 'user', 'activity_type', 'duration', 'distance',
        'calories_burned', 'intensity', 'date', 'created_at'
    )
    list_filter = (
        'activity_type', 'intensity', 'date', 'created_at',
        'user__username'
    )
    search_fields = (
        'title', 'description', 'user__username', 'user__email',
        'location'
    )
    readonly_fields = ('created_at', 'updated_at', 'pace', 'speed')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Activity Details', {
            'fields': (
                'activity_type', 'title', 'description',
                'intensity', 'date', 'start_time', 'location'
            )
        }),
        ('Performance Metrics', {
            'fields': (
                'duration', 'distance', 'calories_burned',
                'pace', 'speed'
            )
        }),
        ('Heart Rate Data', {
            'fields': ('average_heart_rate', 'max_heart_rate'),
            'classes': ('collapse',)
        }),
        ('Additional Data', {
            'fields': ('elevation_gain',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        return super().get_queryset(request).select_related('user')
    
    # Custom admin actions
    actions = ['duplicate_activity']
    
    def duplicate_activity(self, request, queryset):
        """
        Duplicate selected activities
        """
        for activity in queryset:
            activity.pk = None
            activity.title = f"{activity.title} (Copy)"
            activity.save()
        
        self.message_user(
            request,
            f"{queryset.count()} activities duplicated successfully."
        )
    
    duplicate_activity.short_description = "Duplicate selected activities"
