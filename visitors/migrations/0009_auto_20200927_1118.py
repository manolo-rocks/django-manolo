# Generated by Django 3.1.1 on 2020-09-27 10:18

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations
from django.contrib.postgres.search import SearchVector


def update_full_name_dni_host_name(apps, schema_editor):
    model = apps.get_model('visitors', 'Visitor')
    model.objects.update(
        full_name_dni_host_name=SearchVector('full_name', 'id_number', 'host_name')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0008_auto_20180729_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='full_name_dni_host_name',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.RunPython(
            update_full_name_dni_host_name, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddIndex(
            model_name='visitor',
            index=django.contrib.postgres.indexes.GinIndex(
                fields=['full_name_dni_host_name'], name='full_name_dni_host_name_idx'
            ),
        ),
    ]
