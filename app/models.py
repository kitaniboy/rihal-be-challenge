from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=200)
    upload_datetime = models.DateTimeField()
    number_of_pages = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    sentences = models.TextField()
