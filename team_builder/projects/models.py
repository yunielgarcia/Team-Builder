from django.conf import settings
from django.db import models
from accounts.models import Skill


# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="projects")
    title = models.CharField(max_length=140)
    description = models.TextField()

    def __str__(self):
        return self.title


class Position(models.Model):
    skill = models.ForeignKey(Skill, related_name='positions')
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='positions')

    def __str__(self):
        return self.skill
