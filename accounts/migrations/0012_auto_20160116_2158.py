# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160114_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='quarter',
        ),
        migrations.AddField(
            model_name='listing',
            name='fall_quarter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='spring_quarter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='summer_quarter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='winter_quarter',
            field=models.BooleanField(default=False),
        ),
    ]
