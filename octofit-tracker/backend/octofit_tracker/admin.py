from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'team_id', 'created_at']
    list_filter = ['team_id', 'created_at']
    search_fields = ['username', 'email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['activity_type', 'user_id', 'duration', 'calories_burned', 
                    'distance', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['user_id', 'activity_type', 'notes']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['rank', 'username', 'team_name', 'total_activities', 
                    'total_calories', 'total_distance', 'total_duration', 'updated_at']
    list_filter = ['team_name', 'rank']
    search_fields = ['username', 'team_name']
    ordering = ['rank']
    readonly_fields = ['updated_at']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'activity_type', 'difficulty', 'duration', 
                    'calories_estimate', 'created_at']
    list_filter = ['activity_type', 'difficulty']
    search_fields = ['name', 'description', 'activity_type']
    ordering = ['name']
    readonly_fields = ['created_at']
