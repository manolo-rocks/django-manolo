# Generated by Django 4.2.11 on 2024-03-22 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visitors", "0025_auto_20210908_1641"),
    ]

    operations = [
        migrations.AddField(
            model_name="developer",
            name="project_leader",
            field=models.BooleanField(default=False),
        ),
    ]
