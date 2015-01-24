# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='id_number',
            field=models.CharField(help_text='Id number. It should be char field as some numbers begin with zero.', max_length=250),
            preserve_default=True,
        ),
    ]
