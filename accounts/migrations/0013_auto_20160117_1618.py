# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20160116_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='amenities_included',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='amenities_price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='prefered_payment_method',
        ),
    ]
