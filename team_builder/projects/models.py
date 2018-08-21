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


class Skill(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Position(models.Model):
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='positions')
    skill = models.OneToOneField(Skill)

    def __str__(self):
        return self.skill
