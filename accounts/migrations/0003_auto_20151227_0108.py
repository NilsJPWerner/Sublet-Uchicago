# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_listing_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='amenities_included',
            field=models.TextField(blank=True, choices=[(b'yes', b'Yes'), (b'no', b'No')]),
        ),
        migrations.AddField(
            model_name='listing',
            name='amenities_price',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
