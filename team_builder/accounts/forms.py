from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("email", "password1", "password2")
        model = get_user_model()


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
                        attrs={'placeholder': 'enter your bio...'}))
    display_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Display name'},
        )
    )

    class Meta:
        model = get_user_model()
        fields = (
            'display_name',
            'bio',
            'avatar',
        )


class UserSkillForm(forms.ModelForm):
    class Meta:
        fields = ("skill",)
        model = models.UserSkill


UserSkillFormSet = forms.modelformset_factory(
    models.UserSkill,
    form=UserSkillForm,
    extra=1,
)

