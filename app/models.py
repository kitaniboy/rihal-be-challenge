from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    upload_datetime = models.DateTimeField()
    number_of_pages = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    sentences = models.TextField()
