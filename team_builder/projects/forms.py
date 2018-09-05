from django import forms
from django.forms import inlineformset_factory

from . import models


class ProjectForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'circle--input--h1',
               'placeholder': 'Project Title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'project description...'}))
    time_line_description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'circle--textarea--input',
               'placeholder': 'Time estimate'}))

    class Meta:
        model = models.Project
        fields = (
            'title',
            'description',
            'time_line_description',
            'applicant_req'
        )


class PositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = (
            'position_title',
            'skill',
            'description'
        )


# class BaseInlinePositionFormSet(forms.BaseInlineFormSet):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.queryset is None:  # this is odd !!!
    #         self.queryset = models.Position.objects.none()


PositionFormSet = inlineformset_factory(models.Project,
                                        models.Position,
                                        form=PositionForm,
                                        extra=1,
                                        can_delete=True)
