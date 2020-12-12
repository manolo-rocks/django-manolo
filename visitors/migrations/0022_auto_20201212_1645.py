# Generated by Django 2.2.13 on 2020-12-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0021_statistic_updated_institutions'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorScrapeProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_count', models.IntegerField()),
                ('cutoff_date', models.DateField(db_index=True)),
            ],
        ),
        migrations.AlterField(
            model_name='visitor',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
