"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import os
from .views import (
    UserViewSet, TeamViewSet, ActivityViewSet, 
    LeaderboardViewSet, WorkoutViewSet
)

# API Router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view that provides links to all available endpoints
    """
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'endpoints': {
            'users': f'{base_url}/api/users/',
            'teams': f'{base_url}/api/teams/',
            'activities': f'{base_url}/api/activities/',
            'leaderboard': f'{base_url}/api/leaderboard/',
            'workouts': f'{base_url}/api/workouts/',
            'admin': f'{base_url}/admin/',
        },
        'documentation': {
            'users': {
                'list': 'GET /api/users/',
                'detail': 'GET /api/users/{id}/',
                'by_email': 'GET /api/users/by_email/?email={email}',
                'by_team': 'GET /api/users/?team_id={team_id}',
            },
            'teams': {
                'list': 'GET /api/teams/',
                'detail': 'GET /api/teams/{id}/',
                'members': 'GET /api/teams/{id}/members/',
                'stats': 'GET /api/teams/{id}/stats/',
            },
            'activities': {
                'list': 'GET /api/activities/',
                'detail': 'GET /api/activities/{id}/',
                'recent': 'GET /api/activities/recent/',
                'by_user': 'GET /api/activities/?user_id={user_id}',
                'by_type': 'GET /api/activities/?activity_type={type}',
            },
            'leaderboard': {
                'list': 'GET /api/leaderboard/',
                'detail': 'GET /api/leaderboard/{id}/',
                'top': 'GET /api/leaderboard/top/?limit={n}',
                'by_team': 'GET /api/leaderboard/?team_id={team_id}',
            },
            'workouts': {
                'list': 'GET /api/workouts/',
                'detail': 'GET /api/workouts/{id}/',
                'suggest': 'GET /api/workouts/suggest/?activity_type={type}&difficulty={level}',
                'by_type': 'GET /api/workouts/?activity_type={type}',
                'by_difficulty': 'GET /api/workouts/?difficulty={level}',
            }
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root-alt'),
    path('api/', include(router.urls)),
]
