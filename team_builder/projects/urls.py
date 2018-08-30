from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.AllProjects.as_view(), name="all"),
    url(r"(?P<pk>\d+)$", views.ProjectDetailView.as_view(), name="detail_project"),
    url(r"new/$", views.CreateProjectPositionView.as_view(), name="create_project"),
]
