# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20160126_0512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='listing_name',
            new_name='name',
        ),
    ]
