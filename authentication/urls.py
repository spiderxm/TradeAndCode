from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('components/', components_screen, name="components"),
    path('developers/', developers, name="developers"),
    path('not-started/', notStarted, name="notStarted"),
    path('question/', question, name="question"),
    path('register/', register, name="register"),
]
