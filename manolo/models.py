from django.db import models


class Manolo(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.CharField(max_length=250)
    sha512 = models.CharField(max_length=200)
    visitor = models.CharField(max_length=250)
    meeting_place = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    entity = models.CharField(max_length=250)
    objective = models.CharField(max_length=250)
    id_document = models.CharField(max_length=250)
    date = models.DateField(null=True)
    time_start = models.CharField(max_length=100)
    time_end = models.CharField(max_length=100)
