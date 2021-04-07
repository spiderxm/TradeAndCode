import uuid
from datetime import datetime

from django.db.models import Max
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import ContestForm, ComponentsForm, RoundForm, QuestionForm, ContestFormForEdit, SubmissionForm, \
    priceUpdateForm
from models.models import Contest, Round, Question, Components, Submission, Transaction, SubmissionComponents, \
    PlayerTeam, Team
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


@login_required
@staff_member_required
def GetContests(request):
    """
    Get Contest Page - (With all Contests)
    """
    contests = Contest.objects.all()
    return render(request, "details/contests.html", {"docTitle": "Contests", "contests": contests})


class CreateContest(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    This View Handles the Creation of Contest
    """
    permission_required = "auth.admin"

    def get(self, request):
        """
        Get Create Contest Page (with form)
        """
        context = dict()
        context["docTitle"] = "Create Contest"
        form = ContestForm()
        context["form"] = form
        return render(request, "add/createContest.html", context=context)

    def post(self, request):
        """
        Post request to create contest data
        """
        print(request.POST)
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = Contest.objects.create(
                rounds=int(request.POST["rounds"]),
                description=request.POST["description"],
                date=request.POST["date"],
                start_time=request.POST["start_time"],
                money_at_start=request.POST["money_at_start"],
                end_time=request.POST["end_time"]
            )
            contest.save()
            rounds = contest.rounds
            for i in range(1, rounds + 1):
                round = Round.objects.create(
                    id=uuid.uuid4(),
                    contestId=contest,
                    roundNumber=i,
                    roundName=f"Round {str(i)}"
                )
                round.save()
                Question.objects.create(
                    id=uuid.uuid4(),
                    roundId=round,
                ).save()
        else:
            return render(request, "add/createContest.html", context={"form": form, "docTitle": "Create Contest"})
        return HttpResponseRedirect(reverse_lazy('ContestsList'))


class UpdateContest(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    This View Handles to update Contest details
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Update Contest Page (with form)
        """
        contest = get_object_or_404(Contest, pk=id)
        form = ContestFormForEdit(instance=contest)
        return render(request, "update/updateContest.html", context={"form": form, "docTitle": "Edit Contest"})

    def post(self, request, id):
        """
        Post request to update contest data
        """
        form = ContestFormForEdit(request.POST)
        if form.is_valid():
            contest = get_object_or_404(Contest, pk=id)
            contest.description = request.POST["description"]
            contest.start_time = request.POST["start_time"]
            contest.date = request.POST["date"]
            contest.save()
        else:
            return render(request, "update/updateContest.html", {"message": form.errors, "form": form})
        return HttpResponseRedirect(reverse_lazy('ContestsList'))


class DeleteContest(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    This View Handles the Deletion of Contest
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Delete Contest Page (with form)
        """
        contest = get_object_or_404(Contest, pk=id)
        return render(request, "delete/contest.html", {"docTitle": "Delete Contest"})

    def post(self, request, id):
        """
        Post request to delete contest data
        """
        contest = get_object_or_404(Contest, pk=id)
        contest.delete()
        return HttpResponseRedirect(reverse_lazy("ContestsList"))


class DeleteComponent(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    This View Handles the Deletion of Component
    """

    def get(self, request, id):
        """
        Get Delete Component Page (with form)
        """
        component = get_object_or_404(Components, pk=id)
        return render(request, "delete/component.html", {"docTitle": "Delete Component"})

    def post(self, request, id):
        """
        Post request to delete component data
        """
        component = get_object_or_404(Components, pk=id)
        contestId = component.contestId.id
        component.delete()
        return HttpResponseRedirect(reverse_lazy("contest-details", kwargs={"id": contestId}))


class ContestDetails(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Contest Details
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Request to get Details of Contest
        """
        contest = Contest.objects.get(id=id)
        rounds = Round.objects.filter(contestId__id=id)
        components = Components.objects.filter(contestId__id=id)
        context = {
            "rounds": rounds, "contest": contest, "components": components, "docTitle": "Contest Details"
        }
        return render(request, "detail/contests.html", context=context)


class RoundDetails(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Round Details
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Request to get Question Details
        """
        round = Round.objects.get(id=id)
        question = Question.objects.get(roundId=id)
        submissions = Submission.objects.filter(roundId=id)
        context = {
            "round": round,
            "question": question,
            "submissions": submissions,
            "docTitle": "Round Details"
        }
        return render(request, "detail/round.html", context=context)


class CreateComponents(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Create Components
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Create Components Page (with form)
        """
        form = ComponentsForm()
        context = {
            "form": form,
            "docTitle": "Create Component"
        }
        return render(request, "add/createComponents.html", context=context)

    def post(self, request, id):
        """
        Post Request to create components
        """
        form = ComponentsForm(request.POST)
        if form.is_valid():
            component = Components.objects.create(
                contestId_id=id,
                componentName=request.POST["componentName"],
                componentDescription=request.POST["componentDescription"],
                componentPrice=request.POST["componentPrice"]
            )
            component.save()
        else:
            context = {
                "form": form,
                "docTitle": "Create Component",
                "message": form.errors
            }
            return render(request, "add/createComponents.html", context=context)
        return HttpResponseRedirect(reverse_lazy('contest-details', kwargs={"id": id}))


class UpdateComponents(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to handle Updating of Component Details
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Update Components Page (with form)
        """
        component = get_object_or_404(Components, pk=id)
        form = ComponentsForm(instance=component)
        context = {"form": form,
                   "docTitle": "Update Component"}
        return render(request, "update/updateComponent.html", context=context)

    def post(self, request, id):
        """
        Post Request to Update Components
        """
        component = get_object_or_404(Components, pk=id)
        form = ComponentsForm(request.POST)
        if form.is_valid():
            data = request.POST
            component.componentName = data["componentName"]
            component.componentDescription = data["componentDescription"]
            component.componentPrice = data["componentPrice"]
            component.save()
        else:
            print()
            return render(request, "update/updateComponent.html",
                          {"form": form, "docTitle": "Update Component", "message": form.errors})
        return HttpResponseRedirect(reverse_lazy('contest-details', kwargs={'id': component.contestId.id}))


class UpdateRoundDetails(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to handle Updating of Round Details
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Update Round Page (with form)
        """
        round = get_object_or_404(Round, pk=id)
        form = RoundForm(instance=round)
        return render(request, "update/updateRound.html", {"form": form, "docTitle": "Update Round"})

    def post(self, request, id):
        """
        Post Request to update rounds
        """
        round = get_object_or_404(Round, pk=id)
        form = RoundForm(request.POST)
        if form.is_valid():
            print(request.POST)
            round.roundName = request.POST["roundName"]
            if request.POST["startTime"] != '':
                round.startTime = request.POST["startTime"]
            else:
                round.startTime = None
            round.save()
        else:
            form = RoundForm(request.POST)
            return render(request, "update/updateRound.html",
                          {"form": form, "message": form.errors, "docTitle": "Update Round"})
        return HttpResponseRedirect(reverse_lazy('contest-details', kwargs={"id": round.contestId.id}))


class UpdateQuestion(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Update Question
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Update QuestionsPage (with form)
        """
        question = get_object_or_404(Question, pk=id)
        form = QuestionForm(instance=question)
        return render(request, "update/updateQuestion.html", {"form": form, "docTitle": "Update Question"})

    def post(self, request, id):
        """
        Post Request to update questions
        """
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = request.POST
            question = get_object_or_404(Question, pk=id)
            question.title = data["title"]
            question.description = data["description"]
            question.input = data["input"]
            question.output = data["output"]
            question.test_input = data["test_input"]
            question.test_output = data["test_output"]
            question.save()
        else:
            return render(request, "update/updateQuestion.html",
                          {"form": form, "docTitle": "Update Question", "message": form.errors})
        return HttpResponseRedirect(reverse_lazy('round-details', kwargs={'id': question.roundId.id}))


class CheckSubmission(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Request to handle the functionality to check a question
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        """
        Get Check Submission Form
        """
        submission = get_object_or_404(Submission, pk=id)
        question = Question.objects.get(roundId_id=submission.roundId.id)
        form = SubmissionForm(initial={'points': question.points})
        file = submission.file.open()
        content = file.read()
        file.close()
        code = str(content, 'utf-8').split("\n")
        Code = [" " + codeline for i, codeline in enumerate(code) if codeline is not ""]
        components = SubmissionComponents.objects.filter(submission=submission)
        transactions = Transaction.objects.all().filter(
            team=submission.teamCode).order_by('-datetime')
        playerTeams = PlayerTeam.objects.filter(team=submission.teamCode)
        context = {
            "form": form,
            "submission": submission,
            "docTitle": "Check Submission",
            "question": question,
            "code": Code,
            "components": components,
            "transactions": transactions,
            "players": playerTeams
        }
        return render(request, "update/checkSubmission.html", context=context)

    def post(self, request, id):
        """
        Post Check Submission Form
        """
        submission = get_object_or_404(Submission, pk=id)
        form = SubmissionForm(request.POST)

        if form.is_valid():
            data = request.POST
            submission.points = data["points"]
            submission.checkedOrNot = True
            submission.checkedBy = User.objects.all()[0]
            team = submission.teamCode

            Transaction.objects.create(
                previousBalance=team.coins,
                balance=team.coins + int(data["points"]),
                message=submission.roundId.roundName + " successful marking.",
                changeAmount=int(data["points"]),
                mode='Credit',
                datetime=datetime.now(),
                team=team
            ).save()
            team.coins += int(data["points"])
            team.save()
            submission.save()
        else:
            context = {
                "form": form,
                "submission": submission,
                "docTitle": "Check Form"
            }
            return render(request, "update/checkSubmission.html", context=context)
        return HttpResponseRedirect(reverse_lazy('round-details', kwargs={"id": submission.roundId.id}))


class UpdateComponentsPrice(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for Updating prices for components at one go
    """
    permission_required = "auth.admin"

    def get(self, request, id):
        form = priceUpdateForm()
        contest = get_object_or_404(Contest, pk=id)
        context = {
            "contest": contest,
            "form": form,
            "docTitle": "Update Prices"
        }

        return render(request, "update/updatePrice.html", context=context)

    def post(self, request, id):
        data = request.POST
        components = Components.objects.filter(contestId__id=id)
        for component in components:
            if data["type"] == "incr":
                component.componentPrice = int(float(component.componentPrice) * float(data["factor"]))
            else:
                component.componentPrice = int(float(component.componentPrice) / float(data["factor"]))
            component.save()
        return HttpResponseRedirect(reverse_lazy('ContestsList'))


class LeaderBoardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for Updating prices for components at one go
    """
    permission_required = "auth.admin"

    def get(self, request):
        if len(Contest.objects.all()) == 0:
            return HttpResponseRedirect(reverse_lazy('home'))
        contest = Contest.objects.all()[0]

        maxcoins = Team.objects.all().filter(contest=Contest.objects.all()[0]).aggregate(Max('coins'))
        return render(request, template_name="detail/leaderboard.html", context={
            "teams": Team.objects.all().filter(contest=Contest.objects.all()[0]).order_by("-coins"),
            "maxcoins": maxcoins['coins__max']
        })
