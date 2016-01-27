# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='seller_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='renewals',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='renewed_at',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='status',
        ),
        migrations.AlterField(
            model_name='listing',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
