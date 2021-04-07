import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Contest(models.Model):
    """
    Model used for Coding Competitions
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    description = models.TextField(max_length=4000)
    rounds = models.PositiveSmallIntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    money_at_start = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.date) + " " + str(self.start_time)


class Question(models.Model):
    """
    Model for Questions used during coding Competition
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    roundId = models.ForeignKey("Round", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    input = models.TextField(max_length=256, null=True, blank=True)
    output = models.TextField(max_length=256, null=True, blank=True)
    test_input = models.TextField(max_length=256, null=True, blank=True)
    test_output = models.TextField(max_length=256, null=True, blank=True)
    points = models.PositiveBigIntegerField(default=2500, null=True, blank=True)


class Round(models.Model):
    """
    Model for roundDetails of coding competitions
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    contestId = models.ForeignKey("Contest", on_delete=models.CASCADE)
    roundNumber = models.PositiveSmallIntegerField()
    roundName = models.CharField(max_length=256)
    startTime = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.roundName


class Components(models.Model):
    """
    Model for Components details used during the Competition
    """
    id = models.CharField(max_length=256, default=uuid.uuid1, primary_key=True)
    contestId = models.ForeignKey("Contest", on_delete=models.CASCADE)
    componentName = models.CharField(max_length=256)
    componentDescription = models.TextField(max_length=256)
    componentPrice = models.PositiveBigIntegerField(default=100)

    def __str__(self):
        return str(self.componentName) + " " + str(self.componentPrice)


class Team(models.Model):
    """
    Model for team
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    teamCode = models.CharField(max_length=256, null=False)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    teamName = models.CharField(unique=True, max_length=256)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    coins = models.BigIntegerField(default=10000)
    disqualified = models.BooleanField(default=False)

    def __str__(self):
        return self.teamName


class PlayerTeam(models.Model):
    """
    Model to store team for user for a contest
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    def __str__(self):
        return self.player.username + " " + self.team.teamName


class Submission(models.Model):
    """
    Model for group submissions of Coding Questions
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    roundId = models.ForeignKey("Round", on_delete=models.CASCADE)
    teamCode = models.ForeignKey("Team", on_delete=models.CASCADE)
    languageUsed = models.CharField(max_length=256, null=False)
    timeOfSubmission = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField(default=None, blank=True, null=True)
    checkedOrNot = models.BooleanField(default=False)
    file = models.FileField(upload_to='solutions/')
    checkedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.teamCode.teamName + " " + self.roundId.roundName


class Transaction(models.Model):
    """
    Model for storing transactions
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    message = models.TextField(max_length=1024)
    balance = models.BigIntegerField()
    mode = models.CharField(max_length=256, choices=(('Credit', 'Credit'), ('Debit', 'Debit')))
    datetime = models.DateTimeField(auto_now=True)
    changeAmount = models.BigIntegerField()
    previousBalance = models.BigIntegerField()

    def __str__(self):
        return self.team.teamName + " " + self.message


class TeamComponents(models.Model):
    """
    Model to store components of a team
    """
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.team.teamName + " " + self.component.componentName


class TradeTicket(models.Model):
    """
    Model to store Trade ticket details
    """
    id = models.CharField(max_length=256, default=uuid.uuid4, primary_key=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    availed = models.BooleanField(default=False)
    showOnWall = models.BooleanField(default=False)
    code = models.CharField(max_length=256)
    cost = models.BigIntegerField()


class TicketComponents(models.Model):
    """
    Model to store Trade Ticket Components
    """
    ticket = models.ForeignKey(TradeTicket, on_delete=models.CASCADE)
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.component.componentName + " " + self.ticket.team.teamName


class SubmissionComponents(models.Model):
    """
    Model to store Submission Components
    """
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.component.componentName + " " + self.submission.teamCode.teamCode
