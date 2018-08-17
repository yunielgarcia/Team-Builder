from django.conf import settings
from django.db import models


# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="projects")
    title = models.CharField(max_length=140)
    description = models.TextField()

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='positions')

    def __str__(self):
        return self.title
