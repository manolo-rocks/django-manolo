# -*- coding: utf-8 -*-
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField, Q


class Visitor(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    # combined field for full text search on full_name, id_number, host_name,
    # institution, entity, reason, office, meeting place
    full_search = SearchVectorField(null=True)

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
        null=True,
        db_index=True,
    )
    institution2 = models.ForeignKey(
        'Institution', on_delete=models.SET_NULL, null=True, db_index=True
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
        db_index=True,
    )

    id_document = models.CharField(
        max_length=250,
        help_text='Identification document',
        null=True,
    )

    date = models.DateField(
        null=True,
    )

    time_start = models.CharField(
        max_length=250,
        null=True,
    )

    time_end = models.CharField(
        max_length=250,
        null=True,
    )
    censored = models.BooleanField(
        default=False,
        help_text='If True, the visitor is not shown in the search results.',
        db_index=True,
    )

    created = models.DateTimeField()
    modified = models.DateTimeField()

    @classmethod
    def get_full_search_vector(cls):
        return SearchVector(
            'full_name', 'id_number', 'host_name', 'institution',
            'entity', 'reason', 'office', 'meeting_place', 'host_title',
            'location'
        )

    def save(self, *args, **kwargs):
        """Need to update the combined field for full text search"""
        super(Visitor, self).save(*args, **kwargs)
        if not self.full_search:
            Visitor.objects.filter(
                id=self.id
            ).update(
                full_search=self.get_full_search_vector()
            )

    class Meta:
        indexes = [
            GinIndex(
                fields=['full_search'], name='full_search_idx'
            ),
            models.Index(fields=['institution2'], name='institution2_idx'),
            # partial index specifically for IS NULL queries
            models.Index(
                fields=['institution2'],
                name='institution2_not_null_idx',
                condition=Q(institution2__isnull=True)
            ),
        ]


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration = models.DateField(blank=False)
    avatar = models.TextField(
        blank=True,
    )
    credits = models.IntegerField(null=True)


class VisitorScrapeProgress(models.Model):
    """Keep track of number of visitors kept in our db per date

    Keep stats 1 per month or when we reach milestones:
    - 0
    - 10k
    - 100k
    - 1 million
    - then every 1 million
    """
    visitor_count = models.IntegerField()
    cutoff_date = models.DateField(db_index=True)


class Statistic(models.Model):
    data = models.TextField(null=True)
    visitor_count = models.IntegerField(null=True)
    updated_institutions = JSONField(blank=True, null=True)


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
    project_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Institution(models.Model):
    slug = models.CharField(null=False, max_length=200, unique=True)
    name = models.CharField(null=False, max_length=200, unique=True)
    rank = models.IntegerField(default=0)
    font_awesome_icon = models.CharField(null=True)
    ruc = models.CharField(null=True, max_length=200, unique=True)

    def __str__(self):
        return f"{self.slug} ({self.name})"


class KnownCandidate(models.Model):
    """Model to store known candidates in otorongo.club with their full name and DNI."""
    dni = models.CharField(max_length=200, unique=True, db_index=True)
    full_name = models.TextField(null=False)
    first_names = models.TextField(null=False)
    last_names = models.TextField(null=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Known Candidate"
        verbose_name_plural = "Known Candidates"

    def get_otorongo_url(self):
        # This is based on the actual URL pattern in Otorongo
        return f"https://otorongo.club/candidate/{self.dni}/"

    def __str__(self):
        return f"{self.full_name} ({self.dni})"
