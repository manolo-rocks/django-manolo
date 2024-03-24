from django.db import models


class Cazador(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.TextField()
    raw_data = models.TextField()
    raw_data_with_short_links = models.TextField()
