# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 18:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0005_auto_20170607_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='coal_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 429832), verbose_name='Coal bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='food_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 429877), verbose_name='Food bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='iron_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 429786), verbose_name='Iron bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='oil_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 429735), verbose_name='Oil bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='plus_account',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 429677), verbose_name='Plus Account'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 437881)),
        ),
        migrations.AlterField(
            model_name='queue',
            name='next_update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 417364)),
        ),
        migrations.AlterField(
            model_name='village',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 18, 4, 17, 425420), null=True, verbose_name='Last update time'),
        ),
    ]