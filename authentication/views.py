from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Max
from models.models import *
from models.models import Contest, Team, PlayerTeam, Components
from datetime import datetime
from django.contrib import messages


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
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")
    maxcoins = Team.objects.all().filter(contest=Contest.objects.all()[0]).aggregate(Max('coins'))
    return render(request, template_name="leaderboard.html", context={
        "teams": Team.objects.all().filter(contest=Contest.objects.all()[0]).order_by("-coins"),
        "maxcoins": maxcoins['coins__max']
    })


def components_screen(request):
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")
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
    team = None
    players = []

    if len(PlayerTeam.objects.all().filter(player=request.user, contest=Contest.objects.all()[0])) != 0:
        isalreadyinTeam = True
        team = PlayerTeam.objects.all().get(player=request.user, contest=Contest.objects.all()[0]).team
        players = PlayerTeam.objects.all().filter(team=team)
    else:
        contest = Contest.objects.all()[0]
        date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                        minute=contest.start_time.minute, hour=contest.start_time.hour)

        if datetime.now() > date:
            return render(request, template_name="started.html")
        isalreadyinTeam = False
    return render(request, template_name="register.html",
                  context={"isalreadyinTeam": isalreadyinTeam, "team": team, "players": players,
                           "numberOfPlayers": len(players)})


@login_required()
def createTeam(request):
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if datetime.now() > date:
        return render(request, template_name="started.html")
    if len(PlayerTeam.objects.all().filter(player=request.user, contest=Contest.objects.all()[0])) != 0:
        return HttpResponseRedirect(reverse_lazy('register'))
    if request.method == "POST":
        data = request.POST
        teamName = request.POST['teamName']
        teamName = str(teamName).upper()
        if len(Team.objects.all().filter(teamName=str(teamName).strip(), contest=Contest.objects.all()[0])) == 0:
            team = Team.objects.create(
                teamName=teamName,
                teamCode=teamName + str(uuid.uuid1())[:5],
                contest=Contest.objects.all()[0],
                createdBy=request.user,
                coins=Contest.objects.all()[0].money_at_start
            )
            team.save()
            PlayerTeam.objects.create(
                team=team,
                player=request.user,
                contest=Contest.objects.all()[0]
            ).save()
            messages.success(request, "Team created and joined Successfully.")
            return HttpResponseRedirect(reverse_lazy('register'))
        else:
            messages.error(request, "Team with same name already exists. Try again with another name.")
            return render(request, template_name="createTeam.html")

    if request.method == "GET":
        return render(request, template_name="createTeam.html")


@login_required
def joinTeam(request):
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if datetime.now() > date:
        return render(request, template_name="started.html")
    if len(PlayerTeam.objects.all().filter(player=request.user, contest=Contest.objects.all()[0])) != 0:
        return HttpResponseRedirect(reverse_lazy('register'))

    if request.method == "POST":
        data = request.POST
        teamCode = request.POST['teamCode']
        if len(Team.objects.all().filter(teamCode=str(teamCode).strip(), contest=Contest.objects.all()[0])) != 0:
            team = Team.objects.all().get(teamCode=str(teamCode).strip(), contest=Contest.objects.all()[0])
            if len(PlayerTeam.objects.all().filter(team=team)) >= 3:
                messages.error(request, "Team already full. Join another team.")
                return HttpResponseRedirect(reverse_lazy('joinTeam'))
            else:
                PlayerTeam.objects.create(
                    team=team,
                    player=request.user,
                    contest=Contest.objects.all()[0],
                    id=uuid.uuid1()
                ).save()
                messages.success(request, "Successfully joined team")
                return HttpResponseRedirect(reverse_lazy('register'))
        else:
            messages.error(request, "Invalid Team Code. Try again with valid one")
            return HttpResponseRedirect(reverse_lazy('joinTeam'))
    if request.method == "GET":
        return render(request, template_name="joinTeam.html")


@login_required
def round_screen(request):
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")

    rounds = Round.objects.all().filter(contestId=contest.id)

    return render(request, "rounds.html", {"rounds": rounds})


@login_required
def question_screen(request, id):
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")
    try:
        question = Question.objects.all().get(roundId=id)
        round = Round.objects.all().get(id=id)
        return render(request, "question.html", {"question": question, "round": round})
    except:
        return render(request, "404.html")
