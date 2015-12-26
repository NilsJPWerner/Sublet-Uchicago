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
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100, blank=True)),
                ('last_name', models.CharField(max_length=100, blank=True)),
                ('profile_picture', models.ImageField(default=b'/static/img/accounts/empty-photo.png', upload_to=b'profile_pictures', blank=True)),
                ('phone_number', models.CharField(max_length=20, blank=True)),
                ('uni_division', models.CharField(blank=True, max_length=50, choices=[(b'NA', b'Not Affiliated'), (b'first', b'First Year'), (b'second', b'Second Year'), (b'third', b'Third Year'), (b'fourth', b'Fourth Year'), (b'grad', b'Graduate Student'), (b'faculty', b'Faculty Member'), (b'other', b'Other division')])),
                ('description', models.TextField(blank=True)),
                ('user', models.OneToOneField(null=True, default=b'0', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listing_name', models.CharField(max_length=40, blank=True)),
                ('summary', models.TextField(max_length=400, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('latitude', models.DecimalField(default=Decimal('41.796661999999997760824044235050678253173828125'), max_digits=9, decimal_places=6)),
                ('longitude', models.DecimalField(default=Decimal('-87.5941830000000010159055818803608417510986328125'), max_digits=9, decimal_places=6)),
                ('bed_size', models.CharField(blank=True, max_length=10, choices=[(b'king', b'King'), (b'queen', b'Queen'), (b'full', b'Full'), (b'twin', b'Twin')])),
                ('roomate_count', models.CharField(blank=True, max_length=5, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5+', b'5+')])),
                ('bathroom', models.CharField(blank=True, max_length=10, choices=[(b'shared', b'Shared'), (b'private', b'Private')])),
                ('ac', models.BooleanField(default=False)),
                ('in_unit_washer_dryer', models.BooleanField(default=False)),
                ('tv', models.BooleanField(default=False)),
                ('cable_tv', models.BooleanField(default=False)),
                ('internet', models.BooleanField(default=False)),
                ('wheel_chair_accessible', models.BooleanField(default=False)),
                ('pets_live_here', models.BooleanField(default=False)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
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
    ]
