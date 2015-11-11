# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=300)),
                ('details', models.TextField(max_length=2000)),
                ('price', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('renewed_at', models.DateTimeField(default=None, null=True)),
                ('renewals', models.IntegerField(default=0)),
                ('published', models.BooleanField(default=True)),
                ('location', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
