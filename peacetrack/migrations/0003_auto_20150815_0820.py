# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacetrack', '0002_auto_20150813_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='meas_cohort',
            field=models.ForeignKey(related_name=b'meas_cohort', to='peacetrack.Cohort'),
        ),
    ]
