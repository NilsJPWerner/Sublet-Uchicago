# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20160117_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
