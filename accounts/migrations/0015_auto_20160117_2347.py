# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20160117_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='roomate_count',
            new_name='roommate_count',
        ),
    ]
