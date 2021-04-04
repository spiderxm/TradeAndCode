from django import forms
from models.models import Contest, Components, Question, Round, Submission


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ContestFormForEdit(forms.ModelForm):
    """
    Form for Contest Model
    """

    class Meta:
        model = Contest
        exclude = ['id', 'rounds']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'})

        }


class ContestForm(forms.ModelForm):
    """
    Form for Contest Model
    """

    class Meta:
        model = Contest
        exclude = ['id']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'})

        }


class ComponentsForm(forms.ModelForm):
    """
    Form for Components Model
    """

    class Meta:
        model = Components
        exclude = ['id', 'contestId']


class QuestionForm(forms.ModelForm):
    """
    Form for Questions
    """

    class Meta:
        model = Question
        exclude = ['id', 'roundId']


class RoundForm(forms.ModelForm):
    """
    Form for Rounds
    """

    class Meta:
        model = Round
        exclude = ['id', 'roundNumber', 'contestId']

        widgets = {
            'startTime': TimeInput(attrs={'type': 'time'}),
        }


class SubmissionForm(forms.ModelForm):
    """
    Form for Submissions
    """

    class Meta:
        model = Submission
        fields = ['points']


choices = (('incr', 'Increment'), ('decr', 'Decrement'))


class priceUpdateForm(forms.Form):
    """
    Form for Price Update for components in one go.
    """

    factor = forms.DecimalField(min_value=1.1, max_value=2)
    type = forms.ChoiceField(choices=choices)
