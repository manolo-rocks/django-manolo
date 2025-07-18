# Generated by Django 5.2.2 on 2025-06-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visitors", "0034_institution_ruc"),
    ]

    operations = [
        migrations.CreateModel(
            name="KnownCandidate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("dni", models.CharField(db_index=True, max_length=200, unique=True)),
                ("full_name", models.TextField()),
                ("first_names", models.TextField()),
                ("last_names", models.TextField()),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Known Candidate",
                "verbose_name_plural": "Known Candidates",
            },
        ),
    ]
