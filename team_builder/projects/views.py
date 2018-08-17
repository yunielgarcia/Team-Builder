from braces.views import SelectRelatedMixin, PrefetchRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic

from . import models


class AllProjects(LoginRequiredMixin, generic.ListView):
    model = models.Project
    prefetch_related = ["position_set"]
