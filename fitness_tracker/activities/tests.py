from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal
from .models import Activity


class ActivityModelTest(TestCase):
    """
    Test cases for Activity model
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='RUNNING',
            duration=30,
            distance=Decimal('5.0'),
            calories_burned=300,
            date=date.today()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.user, self.user)
        self.assertEqual(self.activity.activity_type, 'RUNNING')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, Decimal('5.0'))
    
    def test_activity_str(self):
        """Test string representation"""
        expected = f"{self.user.username} - Running on {date.today()}"
        self.assertEqual(str(self.activity), expected)
    
    def test_pace_calculation(self):
        """Test pace is calculated correctly"""
        expected_pace = round(30 / 5.0, 2)
        self.assertEqual(self.activity.pace, expected_pace)
    
    def test_speed_calculation(self):
        """Test speed is calculated correctly"""
        expected_speed = round(5.0 / (30 / 60), 2)
        self.assertEqual(self.activity.speed, expected_speed)
    
    def test_auto_title_generation(self):
        """Test title is auto-generated if not provided"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='CYCLING',
            duration=45,
            date=date.today()
        )
        self.assertEqual(activity.title, f"Cycling - {date.today()}")


class ActivityAPITest(APITestCase):
    """
    Test cases for Activity API endpoints
    """
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        # Create test activities
        self.activity1 = Activity.objects.create(
            user=self.user,
            activity_type='RUNNING',
            duration=30,
            distance=Decimal('5.0'),
            calories_burned=300,
            date=date.today()
        )
        
        self.activity2 = Activity.objects.create(
            user=self.user,
            activity_type='CYCLING',
            duration=60,
            distance=Decimal('20.0'),
            calories_burned=500,
            date=date.today() - timedelta(days=1)
        )
        
        self.other_activity = Activity.objects.create(
            user=self.other_user,
            activity_type='SWIMMING',
            duration=45,
            distance=Decimal('2.0'),
            calories_burned=400,
            date=date.today()
        )
    
    def test_list_activities_unauthenticated(self):
        """Test that unauthenticated users cannot list activities"""
        url = reverse('activities:activity-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_activities_authenticated(self):
        """Test listing activities for authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # User should only see their activities
    
    def test_create_activity(self):
        """Test creating a new activity"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-list-create')
        data = {
            'activity_type': 'WEIGHTLIFTING',
            'duration': 45,
            'calories_burned': 250,
            'date': date.today().isoformat()
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.filter(user=self.user).count(), 3)
    
    def test_retrieve_activity(self):
        """Test retrieving a specific activity"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-detail', kwargs={'pk': self.activity1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], 'RUNNING')
    
    def test_retrieve_other_user_activity(self):
        """Test that user cannot retrieve another user's activity"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-detail', kwargs={'pk': self.other_activity.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_activity(self):
        """Test updating an activity"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-detail', kwargs={'pk': self.activity1.pk})
        data = {
            'activity_type': 'RUNNING',
            'duration': 40,
            'calories_burned': 350,
            'date': date.today().isoformat()
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.activity1.refresh_from_db()
        self.assertEqual(self.activity1.duration, 40)
        self.assertEqual(self.activity1.calories_burned, 350)
    
    def test_delete_activity(self):
        """Test deleting an activity"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-detail', kwargs={'pk': self.activity1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activity.objects.filter(user=self.user).count(), 1)
    
    def test_filter_by_activity_type(self):
        """Test filtering activities by type"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-list-create')
        response = self.client.get(url, {'activity_type': 'RUNNING'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_filter_by_date_range(self):
        """Test filtering activities by date range"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-list-create')
        response = self.client.get(url, {
            'date_from': (date.today() - timedelta(days=2)).isoformat(),
            'date_to': date.today().isoformat()
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_activity_metrics(self):
        """Test activity metrics endpoint"""
        self.client.force_authenticate(user=self.user)
        url = reverse('activities:activity-metrics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_activities'], 2)
        self.assertEqual(response.data['total_duration'], 90)  # 30 + 60
