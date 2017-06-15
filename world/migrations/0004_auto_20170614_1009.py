# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 10:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20170614_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_update',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='food_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 686506), verbose_name='Food bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='iron_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 686417), verbose_name='Iron bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='oil_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 686369), verbose_name='Oil bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='plus_account',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 686308), verbose_name='Plus Account'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='wood_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 686464), verbose_name='Wood bonus production'),
        ),
        migrations.AlterField(
            model_name='player',
            name='culture_points',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 694406)),
        ),
        migrations.AlterField(
            model_name='queue',
            name='next_update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 672791)),
        ),
        migrations.AlterField(
            model_name='village',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 10, 9, 40, 681888), null=True, verbose_name='Last update time'),
        ),
    ]