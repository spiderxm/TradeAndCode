import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Contest(models.Model):
    """
    Model used for Coding Competitions
    """
    id = models.CharField(max_length=256, default=uuid.uuid4(), primary_key=True)
    description = models.TextField(max_length=4000)
    rounds = models.PositiveSmallIntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    money_at_start = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.date) + " " + str(self.start_time)


class Question(models.Model):
    """
    Model for Questions used during coding Competition
    """
    id = models.CharField(max_length=256, default=uuid.uuid4(), primary_key=True)
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
    id = models.CharField(max_length=256, default=uuid.uuid4(), primary_key=True)
    contestId = models.ForeignKey("Contest", on_delete=models.CASCADE)
    roundNumber = models.PositiveSmallIntegerField()
    roundName = models.CharField(max_length=256)
    startTime = models.TimeField(null=True, blank=True)


class Components(models.Model):
    """
    Model for Components details used during the Competition
    """
    id = models.CharField(max_length=256, default=uuid.uuid4(), primary_key=True)
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
    id = models.CharField(max_length=256, default=uuid.uuid4(), primary_key=True)
    teamCode = models.CharField(max_length=256, null=False)
    createdBy = models.CharField(max_length=256)
    teamName = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.teamName


class Submission(models.Model):
    """
    Model for group submissions of Coding Questions
    """
    id = models.CharField(max_length=256, default=uuid.uuid4(), primary_key=True)
    roundId = models.ForeignKey("Round", on_delete=models.CASCADE)
    teamCode = models.ForeignKey("Team", on_delete=models.PROTECT)
    fileUrl = models.URLField(max_length=256, null=False)
    languageUsed = models.CharField(max_length=256, null=False)
    timeOfSubmission = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField(default=None, blank=True, null=True)
    checkedOrNot = models.BooleanField(default=False)
    checkedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
