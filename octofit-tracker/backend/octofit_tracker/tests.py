from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from .models import User, Team, Activity, Leaderboard, Workout


class TeamModelTest(TestCase):
    """Tests for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertIsNotNone(self.team._id)
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class UserModelTest(TestCase):
    """Tests for User model"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='password123',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.team_id, str(self.team._id))
        self.assertIsNotNone(self.user._id)
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')


class ActivityModelTest(TestCase):
    """Tests for Activity model"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='password123',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=5.0,
            date=timezone.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertIsNotNone(self.activity._id)


class TeamAPITest(APITestCase):
    """Tests for Team API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Marvel Team',
            description='Avengers assemble!'
        )
    
    def test_get_teams_list(self):
        """Test retrieving teams list"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_team_detail(self):
        """Test retrieving a single team"""
        response = self.client.get(f'/api/teams/{self.team._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Marvel Team')
    
    def test_create_team(self):
        """Test creating a new team"""
        data = {
            'name': 'DC Team',
            'description': 'Justice League'
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)


class UserAPITest(APITestCase):
    """Tests for User API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            email='ironman@marvel.com',
            username='Iron Man',
            password='iamironman',
            team_id=str(self.team._id)
        )
    
    def test_get_users_list(self):
        """Test retrieving users list"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_user_detail(self):
        """Test retrieving a single user"""
        response = self.client.get(f'/api/users/{self.user._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'Iron Man')
    
    def test_get_user_by_email(self):
        """Test retrieving user by email"""
        response = self.client.get('/api/users/by_email/', {'email': 'ironman@marvel.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'Iron Man')
    
    def test_filter_users_by_team(self):
        """Test filtering users by team"""
        response = self.client.get('/api/users/', {'team_id': str(self.team._id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITest(APITestCase):
    """Tests for Activity API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='password123',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=5.0,
            date=timezone.now()
        )
    
    def test_get_activities_list(self):
        """Test retrieving activities list"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_activity_detail(self):
        """Test retrieving a single activity"""
        response = self.client.get(f'/api/activities/{self.activity._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], 'Running')
    
    def test_filter_activities_by_user(self):
        """Test filtering activities by user"""
        response = self.client.get('/api/activities/', {'user_id': str(self.user._id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_recent_activities(self):
        """Test retrieving recent activities"""
        response = self.client.get('/api/activities/recent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 10)


class LeaderboardAPITest(APITestCase):
    """Tests for Leaderboard API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='password123',
            team_id=str(self.team._id)
        )
        self.leaderboard = Leaderboard.objects.create(
            user_id=str(self.user._id),
            username='testuser',
            team_id=str(self.team._id),
            team_name='Test Team',
            total_activities=10,
            total_calories=5000,
            total_distance=50.0,
            total_duration=600,
            rank=1
        )
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard list"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_leaderboard_detail(self):
        """Test retrieving a single leaderboard entry"""
        response = self.client.get(f'/api/leaderboard/{self.leaderboard._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_get_top_leaderboard(self):
        """Test retrieving top leaderboard entries"""
        response = self.client.get('/api/leaderboard/top/', {'limit': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 5)


class WorkoutAPITest(APITestCase):
    """Tests for Workout API endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Super Soldier Training',
            description='Captain America workout',
            activity_type='Weightlifting',
            difficulty='Advanced',
            duration=60,
            calories_estimate=500,
            equipment=['Barbell', 'Dumbbells'],
            instructions=['Warm-up', 'Bench press', 'Cool-down']
        )
    
    def test_get_workouts_list(self):
        """Test retrieving workouts list"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_workout_detail(self):
        """Test retrieving a single workout"""
        response = self.client.get(f'/api/workouts/{self.workout._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Super Soldier Training')
    
    def test_filter_workouts_by_activity_type(self):
        """Test filtering workouts by activity type"""
        response = self.client.get('/api/workouts/', {'activity_type': 'Weightlifting'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_workout_suggestions(self):
        """Test getting workout suggestions"""
        response = self.client.get('/api/workouts/suggest/', {
            'activity_type': 'Weightlifting',
            'difficulty': 'Advanced'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 3)


class APIRootTest(APITestCase):
    """Tests for API root endpoint"""
    
    def test_api_root(self):
        """Test API root returns correct structure"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('endpoints', response.data)
        self.assertIn('documentation', response.data)
        self.assertIn('message', response.data)
    
    def test_api_root_alt(self):
        """Test alternative API root path"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('endpoints', response.data)
