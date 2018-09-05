from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from . import forms
from django.views import generic
from braces.views import PrefetchRelatedMixin

from . import models


class AllProjects(LoginRequiredMixin, PrefetchRelatedMixin, generic.ListView):
    model = models.Project
    prefetch_related = ["positions"]


class ProjectDetailView(LoginRequiredMixin, PrefetchRelatedMixin, generic.DetailView):
    model = models.Project
    prefetch_related = ["positions", "applications"]


class CreateProjectPositionView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProjectForm
    model = models.Project
    success_url = reverse_lazy('projects:all')  # todo: change to detailView

    def get_context_data(self, **kwargs):
        data = super(CreateProjectPositionView, self).get_context_data(**kwargs)
        if self.request.POST:
            data_post = self.request.POST
            data['positions'] = forms.PositionFormSet(data_post, prefix='positions')
        else:
            data['positions'] = forms.PositionFormSet(prefix='positions')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions_form_set = context['positions']

        if form.is_valid() and positions_form_set.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()

            for position_form in positions_form_set:
                if (position_form.cleaned_data.get('skill') and
                        position_form.cleaned_data.get('position_title')):
                    position_obj = position_form.save(commit=False)
                    position_obj.project = self.object
                    position_obj.save()
        return super(CreateProjectPositionView, self).form_valid(form)
