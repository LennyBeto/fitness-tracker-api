from rest_framework import serializers
from .models import Activity
from django.contrib.auth.models import User


class ActivitySerializer(serializers.ModelSerializer):
    """
    Main serializer for Activity model
    """
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source='user')
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    intensity_display = serializers.CharField(source='get_intensity_display', read_only=True)
    pace = serializers.ReadOnlyField()
    speed = serializers.ReadOnlyField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_id', 'activity_type', 'activity_type_display',
            'title', 'description', 'duration', 'distance', 'calories_burned',
            'intensity', 'intensity_display', 'date', 'start_time',
            'average_heart_rate', 'max_heart_rate', 'elevation_gain',
            'location', 'pace', 'speed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def validate_date(self, value):
        """
        Validate that activity date is not in the future
        """
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value
    
    def validate(self, attrs):
        """
        Validate heart rate consistency
        """
        avg_hr = attrs.get('average_heart_rate')
        max_hr = attrs.get('max_heart_rate')
        
        if avg_hr and max_hr and avg_hr > max_hr:
            raise serializers.ValidationError({
                'average_heart_rate': 'Average heart rate cannot be greater than max heart rate.'
            })
        
        return attrs


class ActivityCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating activities
    """
    class Meta:
        model = Activity
        fields = [
            'activity_type', 'title', 'description', 'duration',
            'distance', 'calories_burned', 'intensity', 'date',
            'start_time', 'average_heart_rate', 'max_heart_rate',
            'elevation_gain', 'location'
        ]
    
    def create(self, validated_data):
        """
        Create activity with current user
        """
        user = self.context['request'].user
        return Activity.objects.create(user=user, **validated_data)


class ActivitySummarySerializer(serializers.Serializer):
    """
    Serializer for activity summary/metrics
    """
    total_activities = serializers.IntegerField()
    total_duration = serializers.IntegerField(help_text="Total duration in minutes")
    total_distance = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total distance in km")
    total_calories = serializers.IntegerField(help_text="Total calories burned")
    average_duration = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Average duration in minutes")
    average_distance = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Average distance in km")
    average_calories = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Average calories burned")
    most_common_activity = serializers.CharField(allow_null=True)
    activity_breakdown = serializers.DictField(child=serializers.IntegerField())


class ActivityTypeStatsSerializer(serializers.Serializer):
    """
    Serializer for activity type statistics
    """
    activity_type = serializers.CharField()
    count = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    total_distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_calories = serializers.IntegerField()
    average_duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_calories = serializers.DecimalField(max_digits=10, decimal_places=2)