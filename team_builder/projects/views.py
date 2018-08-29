from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from . import forms
from django.views import generic

from . import models


class AllProjects(LoginRequiredMixin, generic.ListView):
    model = models.Project
    prefetch_related = ["position_set"]


class CreateProjectPositionView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProjectForm
    model = models.Project
    success_url = reverse_lazy('projects:all')  # todo: change to detailView

    def get_context_data(self, **kwargs):
        data = super(CreateProjectPositionView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['positions'] = forms.PositionFormSet(self.request.POST)
        else:
            data['positions'] = forms.PositionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positionsFormSet = context['positions']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            if positionsFormSet.is_valid():
                positionsFormSet.instance = self.object
                positionsFormSet.save()
        return super(CreateProjectPositionView, self).form_valid(form)
