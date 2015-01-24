# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sha1', models.CharField(null=True, help_text='Use it as identifier for any record regardless oforigin. It is built with: date + id_number + time_start', max_length=40)),
                ('full_name', models.CharField(help_text='Full name of visitor', max_length=250)),
                ('entity', models.CharField(help_text='Entity that the visitor represents', max_length=250)),
                ('meeting_place', models.CharField(help_text='Location where meeting takes place', max_length=250)),
                ('office', models.CharField(help_text='Office that visitor visits. Some peruvian institutions haveit as `unidad`.', max_length=250)),
                ('host_name', models.CharField(help_text='Name of person that receives visitor', max_length=250)),
                ('reason', models.CharField(help_text='Reason behind the meeting. Some peruvian institutions haveit as `observación`.', max_length=250)),
                ('institution', models.CharField(help_text='Institution visited', max_length=250)),
                ('location', models.CharField(help_text='Location of Institution. Some institution have severallocations. In PCM is know as `sede`.', max_length=250)),
                ('id_number', models.IntegerField(help_text='Id number')),
                ('id_document', models.CharField(help_text='Identification document', max_length=250)),
                ('date', models.DateField(null=True)),
                ('time_start', models.CharField(max_length=250)),
                ('time_end', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
