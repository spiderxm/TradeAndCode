from django.contrib import admin

# Register your models here.
from .models import Contest, Round, Question, Team, Submission, Components, PlayerTeam, Transaction, TicketComponents, \
    TradeTicket, TeamComponents

admin.site.register([
    Contest,
    Round,
    Question,
    Team,
    Submission,
    Components,
    PlayerTeam,
    Transaction,
    TradeTicket,
    TicketComponents,
    TeamComponents
])
