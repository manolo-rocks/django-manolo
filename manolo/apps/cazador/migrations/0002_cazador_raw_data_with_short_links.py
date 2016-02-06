# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cazador', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cazador',
            name='raw_data_with_short_links',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
