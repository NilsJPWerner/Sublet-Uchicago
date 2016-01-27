# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20160117_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='seller_id',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='listing',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
