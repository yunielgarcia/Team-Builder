from braces.views import SelectRelatedMixin, PrefetchRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic

from . import models


class AllProjects(LoginRequiredMixin, generic.ListView):
    model = models.Project
    prefetch_related = ["position_set"]


class CreateProject(LoginRequiredMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = [
        'title',
        'description'
    ]
    model = models.Project

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
