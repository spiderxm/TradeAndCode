from django.contrib import admin

# Register your models here.
from .models import Contest, Round, Question, Team, Submission, Components, PlayerTeam, Transaction

admin.site.register([
    Contest,
    Round,
    Question,
    Team,
    Submission,
    Components,
    PlayerTeam,
    Transaction
])
