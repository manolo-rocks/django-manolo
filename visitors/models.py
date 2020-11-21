# -*- coding: utf-8 -*-
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.contrib.auth.models import User


class Visitor(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    # combined field for full text search on full_name, id_number, host_name
    full_name_dni_host_name = SearchVectorField(null=True)

    sha1 = models.CharField(
        max_length=40,
        null=True,
        help_text='Use it as identifier for any record regardless of'
                  'origin. It is built with: date + id_number + time_start',
        db_index=True,
    )

    full_name = models.TextField(
        help_text='Full name of visitor',
    )

    entity = models.CharField(
        max_length=250,
        help_text='Entity that the visitor represents',
        null=True,
    )

    meeting_place = models.CharField(
        max_length=250,
        help_text='Location where meeting takes place',
        null=True,
    )

    office = models.CharField(
        max_length=250,
        help_text='Office that visitor visits. Some peruvian institutions have'
                  'it as `unidad`.',
        null=True,
    )

    host_name = models.TextField(
        help_text='Name of person that receives visitor',
        null=True,
    )

    host_title = models.TextField(
        help_text='Official title of host: Jefe, Director, etc',
        null=True
    )

    reason = models.TextField(
        help_text='Reason behind the meeting. Some peruvian institutions have'
                  'it as `observación`.',
        null=True,
    )

    institution = models.CharField(
        max_length=250,
        help_text='Institution visited',
        null=True
    )

    location = models.CharField(
        max_length=250,
        help_text='Location of Institution. Some institution have several'
                  'locations. In PCM is know as `sede`.',
        null=True,
    )

    id_number = models.TextField(
        help_text='Id number. DNI. It should be char field as some numbers begin with zero.',
        null=True,
    )

    id_document = models.CharField(
        max_length=250,
        help_text='Identification document',
        null=True,
    )

    date = models.DateField(
        null=True
    )

    time_start = models.CharField(
        max_length=250,
        null=True,
    )

    time_end = models.CharField(
        max_length=250,
        null=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Need to update the combined field for full text search"""
        super(Visitor, self).save(*args, **kwargs)
        if not self.full_name_dni_host_name:
            Visitor.objects.filter(
                id=self.id
            ).update(
                full_name_dni_host_name=SearchVector('full_name', 'id_number', 'host_name')
            )

    class Meta:
        indexes = [
            GinIndex(
                fields=['full_name_dni_host_name'], name='full_name_dni_host_name_idx'
            )
        ]


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration = models.DateField(blank=False)
    avatar = models.TextField(
        blank=True,
    )
    credits = models.IntegerField(null=True)


class Statistic(models.Model):
    data = models.TextField(null=True)


class Statistic_detail(models.Model):
    name = models.TextField(null=True)
    number_of_visits = models.IntegerField(null=True)


class Developer(models.Model):
    name = models.CharField(null=False, max_length=200)
    title = models.TextField(null=True, blank=True)
    twitter = models.CharField(null=True, blank=True, max_length=200)
    github = models.CharField(null=True, blank=True, max_length=200)
    homepage = models.URLField(null=True, blank=True, max_length=200)
    avatar_image_name = models.CharField(null=True, blank=True, max_length=200)
    rank = models.IntegerField()

    def __str__(self):
        return self.name
