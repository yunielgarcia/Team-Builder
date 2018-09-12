from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"all", views.AllProjects.as_view(), name="all"
    ),
    url(
        r"(?P<pk>\d+)$",
        views.ProjectDetailView.as_view(),
        name="detail_project"),
    url(
        r"(?P<pk>\d+)/positions/(?P<position_pk>\d+)/apply$",
        views.CreateApplicationView.as_view(),
        name="apply"),
    url(
        r"new/$",
        views.CreateProjectPositionView.as_view(),
        name="create_project"),
    url(
        r"(?P<pk>\d+)/edit$",
        views.UpdateProjectPositionView.as_view(),
        name="edit_project"),
    url(
        r"applications/$", views.AllApplications.as_view(), name="applications"
    ),
]
