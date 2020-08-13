# Generated by Django 3.0.3 on 2020-08-08 00:05

import api.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=60)),
                ('risk_score', models.IntegerField(blank=True, default=None)),
                ('category_avg', djongo.models.fields.ArrayField(blank=True, model_container=api.models.categories_average, null=True)),
                ('risk_run', djongo.models.fields.ArrayField(blank=True, model_container=api.models.Time, null=True)),
            ],
        ),
    ]