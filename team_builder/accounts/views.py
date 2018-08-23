from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import UserCreateForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from . import models


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileDetailView(generic.DetailView):
    model = models.User
    template_name = "accounts/profile.html"

    def get_object(self, queryset=None):
        return self.get_queryset().get(
            pk=self.request.user.pk
        )


@login_required
def account_redirect(request):
    return redirect('accounts:profile', pk=request.user.pk)


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.User
    template_name_suffix = '_update_form'
    fields = [
        'display_name',
        'bio',
        'avatar'
    ]

    def get_success_url(self):
        return self.request.user.get_absolute_url()

