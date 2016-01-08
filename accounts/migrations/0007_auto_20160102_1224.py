# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_listing_quarter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'listing_photos/%Y/%m/%d')),
                ('description', models.CharField(max_length=100, blank=True)),
                ('is_cover_photo', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='zip_code',
            field=models.IntegerField(blank=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='listing',
            field=models.ForeignKey(to='accounts.Listing'),
        ),
    ]
