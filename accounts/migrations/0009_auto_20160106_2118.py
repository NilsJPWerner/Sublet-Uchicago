# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20160105_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(null=True, upload_to=b'listing_photos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='listing',
            field=models.ForeignKey(to='accounts.Listing', null=True),
        ),
    ]
