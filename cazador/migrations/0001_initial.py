# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cazador',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('raw_data', models.TextField()),
                ('source', models.TextField()),
            ],
        ),
    ]
