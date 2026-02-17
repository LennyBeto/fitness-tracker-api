from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Activity(models.Model):
    """
    Model representing a fitness activity
    """
    
    ACTIVITY_TYPE_CHOICES = [
        ('RUNNING', 'Running'),
        ('CYCLING', 'Cycling'),
        ('SWIMMING', 'Swimming'),
        ('WALKING', 'Walking'),
        ('WEIGHTLIFTING', 'Weightlifting'),
        ('YOGA', 'Yoga'),
        ('HIIT', 'HIIT'),
        ('CROSSFIT', 'CrossFit'),
        ('BOXING', 'Boxing'),
        ('ROWING', 'Rowing'),
        ('PILATES', 'Pilates'),
        ('DANCING', 'Dancing'),
        ('HIKING', 'Hiking'),
        ('BASKETBALL', 'Basketball'),
        ('FOOTBALL', 'Football'),
        ('TENNIS', 'Tennis'),
        ('GOLF', 'Golf'),
        ('OTHER', 'Other'),
    ]
    
    INTENSITY_CHOICES = [
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High'),
        ('EXTREME', 'Extreme'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text="User who logged this activity"
    )
    
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        help_text="Type of fitness activity"
    )
    
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional title for the activity"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Optional description or notes about the activity"
    )
    
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes",
        validators=[MinValueValidator(1)]
    )
    
    distance = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance covered in kilometers",
        validators=[MinValueValidator(0)]
    )
    
    calories_burned = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Estimated calories burned",
        validators=[MinValueValidator(0)]
    )
    
    intensity = models.CharField(
        max_length=10,
        choices=INTENSITY_CHOICES,
        default='MODERATE',
        help_text="Intensity level of the activity"
    )
    
    date = models.DateField(
        default=timezone.now,
        help_text="Date when the activity was performed"
    )
    
    start_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Start time of the activity"
    )
    
    average_heart_rate = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Average heart rate in BPM",
        validators=[MinValueValidator(30), MaxValueValidator(220)]
    )
    
    max_heart_rate = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum heart rate in BPM",
        validators=[MinValueValidator(30), MaxValueValidator(220)]
    )
    
    elevation_gain = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Elevation gain in meters",
        validators=[MinValueValidator(0)]
    )
    
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Location where the activity took place"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Activities'
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} on {self.date}"
    
    @property
    def pace(self):
        """
        Calculate pace (minutes per kilometer) for distance-based activities
        """
        if self.distance and self.distance > 0:
            return round(self.duration / float(self.distance), 2)
        return None
    
    @property
    def speed(self):
        """
        Calculate average speed (km/h) for distance-based activities
        """
        if self.distance and self.duration > 0:
            hours = self.duration / 60
            return round(float(self.distance) / hours, 2)
        return None
    
    def save(self, *args, **kwargs):
        """
        Auto-generate title if not provided
        """
        if not self.title:
            self.title = f"{self.get_activity_type_display()} - {self.date}"
        super().save(*args, **kwargs)