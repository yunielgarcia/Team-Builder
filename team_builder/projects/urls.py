from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.AllProjects.as_view(), name="all")
]
