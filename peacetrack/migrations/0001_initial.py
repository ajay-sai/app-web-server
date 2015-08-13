# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_title', models.CharField(max_length=300)),
                ('activity_desc', models.CharField(max_length=3000)),
                ('activity_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cohort_name', models.CharField(max_length=300)),
                ('cohort_desc', models.CharField(max_length=3000)),
                ('cohort_no_of_members', models.IntegerField()),
                ('cohort_age', models.CharField(max_length=30)),
                ('cohort_males', models.IntegerField()),
                ('cohort_females', models.IntegerField()),
                ('cohort_pos', models.CharField(max_length=30)),
                ('cohort_notes', models.CharField(max_length=3000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goal_name', models.CharField(max_length=300)),
                ('goal_title', models.CharField(max_length=1000)),
                ('goal_stmt', models.CharField(max_length=3000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ind_desc', models.CharField(max_length=3000)),
                ('ind_type_1', models.CharField(default=b'None', max_length=b'100')),
                ('ind_type_2', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meas_title', models.CharField(max_length=300)),
                ('meas_desc', models.CharField(max_length=3000)),
                ('meas_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obj_name', models.CharField(max_length=300)),
                ('obj_title', models.CharField(max_length=1000)),
                ('obj_stmt', models.CharField(max_length=3000)),
                ('obj_goal', models.ForeignKey(related_name=b'obj_goal', to='peacetrack.Goal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outcome_value', models.IntegerField()),
                ('outcome_ind', models.ForeignKey(related_name=b'outcome_ind', to='peacetrack.Indicator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('output_value', models.IntegerField()),
                ('output_ind', models.ForeignKey(related_name=b'output_ind', to='peacetrack.Indicator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=300)),
                ('project_purpose', models.CharField(max_length=3000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PTPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_name', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_name', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sector_name', models.CharField(max_length=300)),
                ('sector_desc', models.CharField(max_length=3000)),
                ('sector_code', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vol_name', models.CharField(max_length=300)),
                ('vol_email', models.CharField(max_length=300)),
                ('vol_activity', models.ManyToManyField(to='peacetrack.Activity')),
                ('vol_cohort', models.ManyToManyField(to='peacetrack.Cohort')),
                ('vol_meas', models.ManyToManyField(to='peacetrack.Measurement')),
                ('vol_ptpost', models.ForeignKey(related_name=b'vol_ptpost', to='peacetrack.PTPost')),
                ('vol_sector', models.ForeignKey(related_name=b'vol_sector', to='peacetrack.Sector')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ptpost',
            name='post_region',
            field=models.ForeignKey(related_name=b'post_region', to='peacetrack.Region'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ptpost',
            name='sector',
            field=models.ManyToManyField(to='peacetrack.Sector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_sector',
            field=models.ForeignKey(related_name=b'project_sector', to='peacetrack.Sector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='output',
            name='output_ptpost',
            field=models.ForeignKey(related_name=b'output_ptpost', to='peacetrack.PTPost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='output',
            name='output_sector',
            field=models.ForeignKey(related_name=b'output_sector', to='peacetrack.Sector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='outcome',
            name='outcome_ptpost',
            field=models.ForeignKey(related_name=b'outcome_ptpost', to='peacetrack.PTPost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='outcome',
            name='outcome_sector',
            field=models.ForeignKey(related_name=b'outcome_sector', to='peacetrack.Sector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='meas_cohort',
            field=models.ForeignKey(related_name=b'meas_cohort', to='peacetrack.Output'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='meas_outcome',
            field=models.ForeignKey(related_name=b'meas_outcome', to='peacetrack.Outcome'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='ind_obj',
            field=models.ForeignKey(related_name=b'ind_obj', to='peacetrack.Objective'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='goal_project',
            field=models.ForeignKey(related_name=b'goal_project', to='peacetrack.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_cohort',
            field=models.ForeignKey(related_name=b'activity_cohort', to='peacetrack.Cohort'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_output',
            field=models.ForeignKey(related_name=b'activity_output', to='peacetrack.Output'),
            preserve_default=True,
        ),
    ]
