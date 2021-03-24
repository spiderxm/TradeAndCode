from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('market/', components_screen, name="market"),
    path('developers/', developers, name="developers"),
    path('not-started/', notStarted, name="notStarted"),
    path('register/', register, name="register"),
    path('createTeam/', createTeam, name="createTeam"),
    path('joinTeam/', joinTeam, name="joinTeam"),
    path('rounds/', round_screen, name="rounds"),
    path('round/<str:id>/question/', question_screen, name="question_screen"),
]
