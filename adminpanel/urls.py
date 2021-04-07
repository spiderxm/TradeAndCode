from django.urls import path, include
from .views import CreateContest, GetContests, UpdateContest, DeleteContest, ContestDetails, UpdateRoundDetails, \
    RoundDetails, UpdateQuestion, CreateComponents, UpdateComponents, DeleteComponent, CheckSubmission, \
    UpdateComponentsPrice, LeaderBoardView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', GetContests, name="ContestsList"),
    path('leaderBoardView/', LeaderBoardView.as_view(), name="leader-boardView"),
    path('create-contest/', CreateContest.as_view(), name="create-contest"),
    path('update-contest/<str:id>', UpdateContest.as_view(), name="update-contest"),
    path('contest-details/<str:id>', ContestDetails.as_view(), name="contest-details"),
    path('delete-contest/<str:id>', DeleteContest.as_view(), name="delete-contest"),
    path('delete-component/<str:id>', DeleteComponent.as_view(), name="delete-component"),
    path('update-round/<str:id>', UpdateRoundDetails.as_view(), name="update-round"),
    path('round-details/<str:id>', RoundDetails.as_view(), name="round-details"),
    path('updatequestion/<str:id>', UpdateQuestion.as_view(), name="update-question"),
    path('updatecomponent/<str:id>', UpdateComponents.as_view(), name="update-component"),
    path('create-components/<str:id>', CreateComponents.as_view(), name="create-components"),
    path('check-submission/<str:id>', CheckSubmission.as_view(), name="check-submission"),
    path('update-price-of-components/<str:id>', UpdateComponentsPrice.as_view(), name="update-components-price"),

]
