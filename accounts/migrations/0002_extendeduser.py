# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
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
    ]
