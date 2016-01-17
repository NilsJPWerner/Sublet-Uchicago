# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160113_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2016, 1, 14, 3, 57, 54, 170786, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 1, 14, 3, 57, 59, 113561, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
