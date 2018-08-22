from django.contrib.auth import logout
from .forms import UserCreateForm
from django.views import generic
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


class ProfileView(generic.DetailView):
    model = models.User
    template_name = "accounts/profile.html"

    def get_object(self, queryset=None):
        return self.get_queryset().get(
            pk=self.request.user.pk
        )