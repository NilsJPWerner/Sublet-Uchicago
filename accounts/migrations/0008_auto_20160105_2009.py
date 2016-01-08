# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20160102_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='zip_code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
