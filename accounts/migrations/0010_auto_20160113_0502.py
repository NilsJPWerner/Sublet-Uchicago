# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20160106_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='address',
            new_name='street_address',
        ),
        migrations.AddField(
            model_name='listing',
            name='apt',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='city',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='country',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='state',
            field=models.CharField(max_length=40, blank=True),
        ),
    ]
