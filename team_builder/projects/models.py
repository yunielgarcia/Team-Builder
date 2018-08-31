from django.conf import settings
from django.db import models
from accounts.models import Skill


# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="projects")
    title = models.CharField(max_length=140)
    description = models.TextField()
    concluded = models.BooleanField(default=False)
    time_line_description = models.TextField(default='')
    applicant_req = models.TextField(default='')

    def __str__(self):
        return self.title


class Position(models.Model):
    position_title = models.CharField(max_length=40)
    skill = models.ForeignKey(Skill, related_name='positions')
    description = models.TextField(default='')
    project = models.ForeignKey(Project, related_name='positions')
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.position_title


class Application(models.Model):
    position = models.ForeignKey(Position, related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applications')
    status = models.CharField(max_length=30, default='processing')

    def __str__(self):
        return '{}-{} application'.format(self.project, self.candidate)
