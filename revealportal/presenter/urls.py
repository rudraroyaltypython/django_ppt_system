# presenter/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('presentation/<int:id>/', views.presentation_view, name='presentation'),
    path('impress/<int:id>/', views.impress_presentation_view, name='impress_presentation'),

    # Gamification / API
    path('api/score/', views.api_submit_score, name='api_submit_score'),
    path('api/leaderboard/', views.api_leaderboard, name='api_leaderboard'),
    path('api/leaderboard/<int:presentation_id>/', views.api_leaderboard, name='api_leaderboard_presentation'),
]
