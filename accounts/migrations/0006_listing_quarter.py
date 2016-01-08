# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_listing_prefered_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='quarter',
            field=models.CharField(blank=True, max_length=10, choices=[(b'summer', b'Summer'), (b'fall', b'Fall'), (b'winter', b'Winter'), (b'spring', b'Spring')]),
        ),
    ]
