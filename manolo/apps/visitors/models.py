# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Visitor(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    sha1 = models.CharField(
        max_length=40,
        null=True,
        help_text='Use it as identifier for any record regardless of'
                  'origin. It is built with: date + id_number + time_start'
    )

    full_name = models.CharField(
        max_length=250,
        help_text='Full name of visitor',
        db_index=True,
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

    host_name = models.CharField(
        max_length=250,
        help_text='Name of person that receives visitor',
        null=True,
    )

    reason = models.CharField(
        max_length=250,
        help_text='Reason behind the meeting. Some peruvian institutions have'
                  'it as `observación`.',
        null=True,
    )

    institution = models.CharField(
        max_length=250,
        help_text='Institution visited',
        null=True,
        db_index=True,
    )

    location = models.CharField(
        max_length=250,
        help_text='Location of Institution. Some institution have several'
                  'locations. In PCM is know as `sede`.',
        null=True,
    )

    id_number = models.CharField(
        max_length=250,
        help_text='Id number. It should be char field as some numbers begin with zero.',
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
    modified = models.DateTimeField(auto_now=True, db_index=True)


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration = models.DateField(blank=False)
    avatar = models.TextField(
        blank=True,
    )
    alerts = models.ManyToManyField('Alert')


class Alert(models.Model):
    full_name = models.TextField(db_index=True, unique=True)
