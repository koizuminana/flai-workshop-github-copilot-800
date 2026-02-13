from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer, 
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    Supports CRUD operations and filtering by team.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        """Override to handle ObjectId lookups"""
        pk = self.kwargs.get('pk')
        try:
            obj_id = ObjectId(pk)
            obj = User.objects.get(_id=obj_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except (User.DoesNotExist, Exception):
            from rest_framework.exceptions import NotFound
            raise NotFound('User not found')
    
    def get_queryset(self):
        """Filter users by team_id if provided"""
        queryset = User.objects.all()
        team_id = self.request.query_params.get('team_id', None)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """Get user by email"""
        email = request.query_params.get('email', None)
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams.
    Supports CRUD operations and member statistics.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    def get_object(self):
        """Override to handle ObjectId lookups"""
        pk = self.kwargs.get('pk')
        try:
            obj_id = ObjectId(pk)
            obj = Team.objects.get(_id=obj_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except (Team.DoesNotExist, Exception):
            from rest_framework.exceptions import NotFound
            raise NotFound('Team not found')
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a team"""
        team = self.get_object()
        users = User.objects.filter(team_id=str(team._id))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics"""
        team = self.get_object()
        members = User.objects.filter(team_id=str(team._id))
        leaderboard_entries = Leaderboard.objects.filter(team_id=str(team._id))
        
        total_activities = sum(entry.total_activities for entry in leaderboard_entries)
        total_calories = sum(entry.total_calories for entry in leaderboard_entries)
        total_distance = sum(entry.total_distance for entry in leaderboard_entries)
        
        return Response({
            'team_name': team.name,
            'member_count': members.count(),
            'total_activities': total_activities,
            'total_calories': total_calories,
            'total_distance': round(total_distance, 2)
        })


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    Supports CRUD operations and filtering by user and activity type.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_object(self):
        """Override to handle ObjectId lookups"""
        pk = self.kwargs.get('pk')
        try:
            obj_id = ObjectId(pk)
            obj = Activity.objects.get(_id=obj_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except (Activity.DoesNotExist, Exception):
            from rest_framework.exceptions import NotFound
            raise NotFound('Activity not found')
    
    def get_queryset(self):
        """Filter activities by user_id and activity_type if provided"""
        queryset = Activity.objects.all().order_by('-date')
        user_id = self.request.query_params.get('user_id', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 10)"""
        activities = Activity.objects.all().order_by('-date')[:10]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard.
    Supports retrieval and filtering by team.
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    
    def get_object(self):
        """Override to handle ObjectId lookups"""
        pk = self.kwargs.get('pk')
        try:
            obj_id = ObjectId(pk)
            obj = Leaderboard.objects.get(_id=obj_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except (Leaderboard.DoesNotExist, Exception):
            from rest_framework.exceptions import NotFound
            raise NotFound('Leaderboard entry not found')
    
    def get_queryset(self):
        """Filter leaderboard by team_id if provided"""
        queryset = Leaderboard.objects.all().order_by('rank')
        team_id = self.request.query_params.get('team_id', None)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N entries from leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        entries = Leaderboard.objects.all().order_by('rank')[:limit]
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts.
    Supports CRUD operations and filtering by activity type and difficulty.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_object(self):
        """Override to handle ObjectId lookups"""
        pk = self.kwargs.get('pk')
        try:
            obj_id = ObjectId(pk)
            obj = Workout.objects.get(_id=obj_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except (Workout.DoesNotExist, Exception):
            from rest_framework.exceptions import NotFound
            raise NotFound('Workout not found')
    
    def get_queryset(self):
        """Filter workouts by activity_type and difficulty if provided"""
        queryset = Workout.objects.all()
        activity_type = self.request.query_params.get('activity_type', None)
        difficulty = self.request.query_params.get('difficulty', None)
        
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def suggest(self, request):
        """Get workout suggestions based on user preferences"""
        activity_type = request.query_params.get('activity_type', None)
        difficulty = request.query_params.get('difficulty', None)
        
        queryset = Workout.objects.all()
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Return up to 3 suggestions without random ordering (Djongo limitation)
        suggestions = list(queryset[:3])
        serializer = self.get_serializer(suggestions, many=True)
        return Response(serializer.data)
