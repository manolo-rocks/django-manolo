from __future__ import unicode_literals

from django.db import models


class Cazador(models.Model):
    id = models.AutoField(primary_key=True)
    raw_data = models.TextField()
    source = models.TextField()
