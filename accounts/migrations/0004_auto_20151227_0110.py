# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151227_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='amenities_included',
            field=models.CharField(blank=True, max_length=10, choices=[(b'yes', b'Yes'), (b'no', b'No')]),
        ),
    ]
