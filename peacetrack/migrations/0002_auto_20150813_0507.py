# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacetrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='ind_type_2',
            field=models.BooleanField(default=False),
        ),
    ]
