from django.db import models
from django.contrib.postgres.fields import ArrayField

class Quiz(models.Model):
    name = models.CharField(max_length=255)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_DEFAULT, related_name="questions", default=None, null=True)
    text = models.CharField(max_length=255)
    is_open_ended = models.BooleanField(default=False)
    answers = ArrayField(models.CharField(max_length=255), default=list)


