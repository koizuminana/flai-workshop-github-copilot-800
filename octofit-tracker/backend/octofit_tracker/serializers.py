from rest_framework import serializers
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    date_joined = serializers.DateTimeField(source='created_at', read_only=True)
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'password', 'fitness_level', 'team_id', 'team_name', 'created_at', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
    
    def get_team_name(self, obj):
        """Get the team name from team_id"""
        if obj.team_id:
            try:
                # Convert string to ObjectId for lookup
                team_object_id = ObjectId(obj.team_id)
                team = Team.objects.get(_id=team_object_id)
                return team.name
            except (Team.DoesNotExist, Exception):
                return None
        return None
    
    def update(self, instance, validated_data):
        """Update user, only updating password if provided"""
        password = validated_data.pop('password', None)
        
        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Only update password if it was provided
        if password:
            instance.password = password
        
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'created_at']
    
    def get_members(self, obj):
        """Get list of users who are members of this team"""
        team_id_str = str(obj._id)
        users = User.objects.filter(team_id=team_id_str)
        return UserSerializer(users, many=True).data
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model with ObjectId conversion"""
    id = serializers.CharField(source='_id', read_only=True)
    name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'name', 'username', 'activity_type', 'duration', 'calories_burned', 
                  'distance', 'date', 'notes']
    
    def get_name(self, obj):
        """Get the user's name from user_id"""
        if obj.user_id:
            try:
                user_object_id = ObjectId(obj.user_id)
                user = User.objects.get(_id=user_object_id)
                return user.name
            except (User.DoesNotExist, Exception):
                return None
        return None
    
    def get_username(self, obj):
        """Get the username from user_id"""
        if obj.user_id:
            try:
                user_object_id = ObjectId(obj.user_id)
                user = User.objects.get(_id=user_object_id)
                return user.username
            except (User.DoesNotExist, Exception):
                return None
        return None
    
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
