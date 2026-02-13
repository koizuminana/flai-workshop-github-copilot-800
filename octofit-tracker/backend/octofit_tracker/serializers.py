from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'team_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'calories_burned', 
                  'distance', 'date', 'notes']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'username', 'team_id', 'team_name', 
                  'total_activities', 'total_calories', 'total_distance', 
                  'total_duration', 'rank', 'updated_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'activity_type', 'difficulty', 
                  'duration', 'calories_estimate', 'equipment', 'instructions', 
                  'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation
