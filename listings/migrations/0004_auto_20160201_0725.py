# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20160127_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bed_size',
            field=models.IntegerField(blank=True, choices=[(b'4', b'King'), (b'3', b'Queen'), (b'2', b'Full'), (b'1', b'Twin')]),
        ),
    ]
