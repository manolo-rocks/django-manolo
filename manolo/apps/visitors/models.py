from django.db import models
import hashlib


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
        help_text='Full name of visitor'
    )

    entity = models.CharField(
        max_length=250,
        help_text='Entity that the visitor represents'
    )

    meeting_place = models.CharField(
        max_length=250,
        help_text='Location where meeting takes place'
    )

    office = models.CharField(
        max_length=250,
        help_text='Office that visitor visits. Some peruvian institutions have'
                  'it as `unidad`.'
    )

    host_name = models.CharField(
        max_length=250,
        help_text='Name of person that receives visitor'
    )

    reason = models.CharField(
        max_length=250,
        help_text='Reason behind the meeting. Some peruvian institutions have'
                  'it as `observación`.'
    )

    institution = models.CharField(
        max_length=250,
        help_text='Institution visited'
    )

    location = models.CharField(
        max_length=250,
        help_text='Location of Institution. Some institution have several'
                  'locations. In PCM is know as `sede`.'
    )

    id_number = models.CharField(
        max_length=250,
        help_text='Id number. It should be char field as some numbers begin with zero.'
    )

    id_document = models.CharField(
        max_length=250,
        help_text='Identification document'
    )

    date = models.DateField(
        null=True
    )

    time_start = models.CharField(
        max_length=250
    )

    time_end = models.CharField(
        max_length=250
    )
