from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('components/', components_screen, name="components"),

]
