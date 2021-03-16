from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models.models import *
# Create your views here.
from models.models import Contest


def home(request):
    return render(request, template_name="home.html", context={
        "contest": Contest.objects.all()[0]
    })


@login_required()
def leaderboard(request):
    return render(request, template_name="leaderboard.html", context={
        "teams": []
    })


@login_required()
def components_screen(request):
    return render(request, template_name="component_screen.html", context={
        "components": Components.objects.all()
    })
