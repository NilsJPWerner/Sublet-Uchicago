# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-28 22:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_auto_20160201_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bed_size',
            field=models.IntegerField(blank=True, choices=[(4, b'King'), (3, b'Queen'), (2, b'Full'), (1, b'Twin')]),
        ),
    ]
