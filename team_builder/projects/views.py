from django.db import transaction
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
            import pdb;pdb.set_trace()
            data['positions'] = forms.PositionFormSet(data=self.request.POST)
        else:
            data['positions'] = forms.PositionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions_form_set = context['positions']

        if form.is_valid() and positions_form_set.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()

            # positions_form_set.instance = self.object
            # positions_form_set.save()
            for position_form in positions_form_set:
                # import pdb;
                # pdb.set_trace()

                if (position_form.cleaned_data.get('skill') and
                        position_form.cleaned_data.get('position_title')):
                    position_obj = position_form.save(commit=False)
                    position_obj.project = self.object
                    position_obj.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return super(CreateProjectPositionView, self).form_valid(form)
