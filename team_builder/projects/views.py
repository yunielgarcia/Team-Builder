from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail

from . import forms
from django.shortcuts import get_object_or_404
from django.views import generic
from braces.views import PrefetchRelatedMixin, SelectRelatedMixin

from . import models


class AllProjects(LoginRequiredMixin, PrefetchRelatedMixin, generic.ListView):
    model = models.Project
    prefetch_related = ["positions"]

    def get_queryset(self):
        if not self.request.GET.get('q'):
            return models.Project.objects.all()
        else:
            return models.Project.objects.filter(
                title__icontains=self.request.GET.get('q')
            )


class ProjectDetailView(LoginRequiredMixin, PrefetchRelatedMixin, generic.DetailView):
    model = models.Project
    prefetch_related = ["positions"]


class CreateProjectPositionView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProjectForm
    model = models.Project

    def get_success_url(self):
        return reverse_lazy('projects:detail_project', kwargs={'pk': self.object.pk})

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


class UpdateProjectPositionView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.ProjectForm
    model = models.Project
    template_name = "projects/project_edit_form.html"

    def get_success_url(self):
        return reverse_lazy('projects:detail_project', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateProjectPositionView, self).get_context_data(**kwargs)
        if self.request.POST:
            data_post = self.request.POST
            self.object = self.get_object()
            data['positions'] = forms.PositionEditFormSet(prefix='positions', data=data_post, instance=self.object)
        else:
            data['positions'] = forms.PositionEditFormSet(prefix='positions', instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions_form_set = context['positions']

        self.object = self.get_object()

        for position_form in positions_form_set:
            if form.is_valid() and position_form.is_valid():

                if position_form.cleaned_data and position_form.cleaned_data['id']:

                    skill = position_form.cleaned_data['skill']
                    description = position_form.cleaned_data['description']
                    position_title = position_form.cleaned_data['position_title']
                    pos = models.Position.objects.get(
                        id=position_form.cleaned_data['id'].id)
                    pos.description = description
                    pos.skill = skill
                    pos.position_title = position_title
                    pos.save()
                else:
                    # Is newly added.
                    position_obj = position_form.save(commit=False)
                    position_obj.project = self.object
                    position_obj.save()

        return super(UpdateProjectPositionView, self).form_valid(form)


class CreateApplicationView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:detail_project', kwargs={'pk': self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        try:
            position = models.Position.objects.get(pk=self.kwargs['position_pk'])
        except models.Position.DoesNotExist:
            messages.warning(
                self.request,
                "You can't apply to this position."
            )
        else:
            models.Application.objects.create(
                position=position,
                candidate=self.request.user)
        return super().get(request, *args, **kwargs)


class AllApplications(LoginRequiredMixin, PrefetchRelatedMixin, generic.ListView):
    model = models.Application
    prefetch_related = ["candidate", "position"]

    def get_queryset(self):
        if self.request.GET.get('p'):
            return models.Application.objects.filter(
                position__project__pk=self.request.GET.get('p')
            )
        else:
            return models.Application.objects.filter(
                position__project__owner=self.request.user
            )


class ApplicationsDetailView(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    model = models.Application
    select_related = ["candidate"]
    # template_name = "application_detail.html"


class AcceptRejectApplicationView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:applications')

    def get_object(self):
        return get_object_or_404(models.Application, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        application = self.get_object()

        # if the person is actually the project owner then accept/reject
        if application.position.project.owner == self.request.user:
            decision = self.kwargs.get('decision')
            application.status = decision
            if decision == 'Accepted':
                application.position.filled = True
                application.position.save()

            application.save()
            send_mail(
                'Decision',
                'Your application has been {}'.format(decision),
                'TeamBuilder.com',
                [application.candidate.email],
                fail_silently=False,
            )
        return super().get(request, *args, **kwargs)

