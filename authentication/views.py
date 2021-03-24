from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Max
from models.models import *
from models.models import Contest, Team, PlayerTeam, Components, Submission, TeamComponents
from datetime import datetime, timedelta
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
    if datetime.now() > date and len(PlayerTeam.objects.all().filter(player=request.user)) == 0:
        return render(request, template_name="started.html")
    if request.method == "GET":
        return render(request, template_name="component_screen.html", context={
            "components": Components.objects.all(),
            "team": PlayerTeam.objects.all().get(player=request.user).team
        })
    else:
        keys = list(request.POST)
        keys.remove('csrfmiddlewaretoken')
        coins = PlayerTeam.objects.get(player=request.user).team.coins
        cost = 0
        for key in keys:
            componentPrice = Components.objects.get(id=key).componentPrice
            cost = cost + componentPrice * int(request.POST[key])

        if cost > coins:
            messages.error(request, "You don't have enough coins to buy components.")
            return HttpResponseRedirect(reverse_lazy('market'))
        if cost == 0:
            messages.error(request, "Please select a component to proceed.")
            return HttpResponseRedirect(reverse_lazy('market'))
        request.session["components"] = request.POST
        request.session["coins"] = cost
        return HttpResponseRedirect(reverse_lazy('confirmTransaction'))


def confirmComponentsSale(request):
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")
    if datetime.now() > date and len(PlayerTeam.objects.all().filter(player=request.user)) == 0:
        return render(request, template_name="started.html")
    if request.method == "GET":
        coins = request.session.get("coins")
        data = request.session.get("components")
        if coins is None and data is None:
            messages.error(request, "Select Elements to continue")
            return HttpResponseRedirect(reverse_lazy('market'))
        del data['csrfmiddlewaretoken']
        components = []
        quantity = []
        for d in data:
            if int(data[d]) != 0:
                components.append(Components.objects.get(id=d))
                quantity.append(data[d])
        return render(request, template_name="confirmComponentTransaction.html", context={
            "coins": coins,
            "components": zip(components, quantity)
        })
    if request.method == "POST":
        coins = request.session.get("coins")
        data = request.session.get("components")
        if coins is None and data is None:
            messages.error(request, "Select Elements to continue")
            return HttpResponseRedirect(reverse_lazy('market'))
        del data['csrfmiddlewaretoken']
        components = []
        team = PlayerTeam.objects.all().get(player=request.user).team
        quantity = []
        for d in data:
            if int(data[d]) != 0:
                components.append(Components.objects.get(id=d))
                quantity.append(int(data[d]))
        if coins > team.coins:
            messages.error(request, "You don't have enough coins to buy components.")
            return HttpResponseRedirect(reverse_lazy('market'))
        if coins == 0:
            messages.error(request, "Please select a component to proceed.")
        Transaction.objects.create(
            message="Bought Components",
            mode="Debit",
            changeAmount=coins,
            previousBalance=team.coins,
            balance=team.coins - coins,
            team=team
        ).save()
        i = 0
        for component in components:
            obj, created = TeamComponents.objects.get_or_create(component=component, team=team)
            obj.quantity += quantity[i]
            obj.save()
            i += 1
        team.coins = team.coins - coins
        team.save()
        messages.success(request, "Components Bought Successfully.")
        del request.session['coins']
        del request.session['components']
        return HttpResponseRedirect(reverse_lazy('register'))


def developers(request):
    return render(request, template_name="developers.html")


@login_required()
def notStarted(request):
    return render(request, template_name="NotStarted.html")


@login_required()
def question(request):
    return render(request, template_name="question.html")


@login_required()
def register(request):
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
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
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if datetime.now() > date:
        return render(request, template_name="started.html")
    if len(PlayerTeam.objects.all().filter(player=request.user, contest=Contest.objects.all()[0])) != 0:
        return HttpResponseRedirect(reverse_lazy('register'))
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamName = str(teamName).upper()
        if len(Team.objects.all().filter(teamName=str(teamName).strip(), contest=Contest.objects.all()[0])) == 0:
            team = Team.objects.create(
                teamName=teamName,
                teamCode=teamName + str(uuid.uuid1())[:5],
                contest=contest,
                createdBy=request.user,
                coins=contest.money_at_start
            )
            team.save()
            Transaction.objects.create(
                message="Initial Amount",
                balance=contest.money_at_start,
                previousBalance=0,
                mode='Credit',
                datetime=datetime.now(),
                team=team,
                changeAmount=contest.money_at_start,
            ).save()
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
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
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

    if len(PlayerTeam.objects.all().filter(player=request.user)) == 0 and datetime.now() > date:
        return render(request, template_name="started.html")

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

    if len(PlayerTeam.objects.all().filter(player=request.user)) == 0 and datetime.now() > date:
        return render(request, template_name="started.html")

    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")

    if request.method == "GET":
        try:
            question = Question.objects.all().get(roundId=id)
            round = Round.objects.all().get(id=id)
            date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                            minute=round.startTime.minute, hour=round.startTime.hour)

            if date > datetime.now():
                return render(request, "RoundNotStarted.html", {"round": round, "date": date})
            date = timedelta(minutes=40) + date
            if date > datetime.now():
                if len(Submission.objects.all().filter(teamCode=PlayerTeam.objects.get(player=request.user).team,
                                                       roundId=round)) == 0:
                    return render(request, "question.html", {"question": question, "round": round, "submission": False})
                else:
                    return render(request, "question.html", {"question": question, "round": round, "submission": True})

            return render(request, "RoundEnded.html", {"round": round, "time": date})
        except:
            return render(request, "404.html")
    if request.method == "POST":
        try:
            question = Question.objects.all().get(roundId=id)
            round = Round.objects.all().get(id=id)
            date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                            minute=round.startTime.minute, hour=round.startTime.hour)
            if date > datetime.now():
                return render(request, "RoundNotStarted.html", {"round": round, "date": date})
            date = timedelta(minutes=40) + date
            Submission.objects.create(
                teamCode=PlayerTeam.objects.get(player=request.user).team,
                file=request.FILES['submission'],
                roundId=round
            ).save()
            print("hello")
            return HttpResponseRedirect(reverse_lazy('question_screen', kwargs={'id': str(id)}))
        except:
            return render(request, "404.html")


@login_required
def transactionHistory(request):
    if len(Contest.objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('home'))
    contest = Contest.objects.all()[0]
    date = datetime(year=contest.date.year, month=contest.date.month, day=contest.date.day,
                    minute=contest.start_time.minute, hour=contest.start_time.hour)

    if date > datetime.now():
        return render(request, "NotStarted.html")
    if len(PlayerTeam.objects.all().filter(player=request.user)) == 0:
        return render(request, "")
    team = PlayerTeam.objects.all().get(player=request.user).team
    transactions = Transaction.objects.all().filter(
        team=team).order_by('datetime')
    return render(request, "transactions.html", {"transactions": transactions, "team": team})
