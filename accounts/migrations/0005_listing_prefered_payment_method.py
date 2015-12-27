# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151227_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='prefered_payment_method',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
