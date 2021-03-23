from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from models.models import *
from models.models import Contest, Team, PlayerTeam, Components, Submission


def home(request):
    if len(Contest.objects.all()) == 0:
        return render(request, template_name="home.html", context={
            "contest": None,
            "contest-present": False
        })
    return render(request, template_name="home.html", context={
        "contest": Contest.objects.all()[0]
    })


@login_required()
def leaderboard(request):
    return render(request, template_name="leaderboard.html", context={
        "teams": []
    })


def components_screen(request):
    return render(request, template_name="component_screen.html", context={
        "components": Components.objects.all()
    })


def developers(request):
    return render(request, template_name="developers.html", context={
    })


@login_required()
def notStarted(request):
    return render(request, template_name="NotStarted.html")


@login_required()
def question(request):
    return render(request, template_name="question.html")


@login_required()
def register(request):
    return render(request, template_name="register.html")


@login_required()
def createTeam(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        teamName = request.POST['teamName']
        if len(Team.objects.all().filter(teamName=str(teamName).split(), contest=Contest.objects.all()[0])) == 0:
            team = Team.objects.create(
                teamName=teamName,
                teamCode=teamName + str(uuid.uuid1())[:5],
                contest=Contest.objects.all()[0],
                createdBy=request.user
            )
            team.save()
            PlayerTeam.objects.create(
                team=team,
                player=request.user,
                contest=Contest.objects.all()[0]
            ).save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return render(request, template_name="createTeam.html")

        return render(request, template_name="createTeam.html")
    if request.method == "GET":
        return render(request, template_name="createTeam.html")


@login_required()
def joinTeam(request):
    if request.method == "POST":
        data = request.POST
        print(data)

    if request.method == "GET":
        return render(request, template_name="joinTeam.html")
