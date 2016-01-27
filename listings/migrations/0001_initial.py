# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listing_name', models.CharField(max_length=40, blank=True)),
                ('summary', models.TextField(max_length=400, blank=True)),
                ('price', models.IntegerField(default=0, blank=True)),
                ('country', models.CharField(max_length=100, blank=True)),
                ('street_address', models.CharField(max_length=100, blank=True)),
                ('apt', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=100, blank=True)),
                ('state', models.CharField(max_length=40, blank=True)),
                ('zip_code', models.IntegerField(null=True, blank=True)),
                ('latitude', models.DecimalField(default=Decimal('41.796661999999997760824044235050678253173828125'), max_digits=9, decimal_places=6)),
                ('longitude', models.DecimalField(default=Decimal('-87.5941830000000010159055818803608417510986328125'), max_digits=9, decimal_places=6)),
                ('bed_size', models.CharField(blank=True, max_length=10, choices=[(b'king', b'King'), (b'queen', b'Queen'), (b'full', b'Full'), (b'twin', b'Twin')])),
                ('roommate_count', models.CharField(blank=True, max_length=5, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5+', b'5+')])),
                ('bathroom', models.CharField(blank=True, max_length=10, choices=[(b'shared', b'Shared'), (b'private', b'Private')])),
                ('ac', models.BooleanField(default=False)),
                ('in_unit_washer_dryer', models.BooleanField(default=False)),
                ('tv', models.BooleanField(default=False)),
                ('cable_tv', models.BooleanField(default=False)),
                ('internet', models.BooleanField(default=False)),
                ('wheel_chair_accessible', models.BooleanField(default=False)),
                ('pets_live_here', models.BooleanField(default=False)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('fall_quarter', models.BooleanField(default=False)),
                ('winter_quarter', models.BooleanField(default=False)),
                ('spring_quarter', models.BooleanField(default=False)),
                ('summer_quarter', models.BooleanField(default=False)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('renewed_at', models.DateTimeField(auto_now=True, null=True)),
                ('renewals', models.IntegerField(default=0)),
                ('published', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=300)),
                ('seller_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'listing_photos/%Y/%m/%d')),
                ('description', models.CharField(max_length=100, null=True, blank=True)),
                ('is_cover_photo', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(to='listings.Listing', null=True)),
            ],
        ),
    ]
