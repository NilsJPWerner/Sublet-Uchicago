# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-02 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_extendeduser_starred'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='home_town',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
