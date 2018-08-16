from braces.views import SelectRelatedMixin, PrefetchRelatedMixin
from django.views import generic

from . import models


class AllProjects(generic.ListView):
    model = models.Project
    prefetch_related = ["position_set"]
