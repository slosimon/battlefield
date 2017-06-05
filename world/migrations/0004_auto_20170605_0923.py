# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 09:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20170604_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='coal_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 66180), verbose_name='Coal bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='food_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 66257), verbose_name='Food bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='iron_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 66101), verbose_name='Iron bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='oil_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 66018), verbose_name='Oil bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='plus_account',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 65922), verbose_name='Plus Account'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 78028)),
        ),
        migrations.AlterField(
            model_name='village',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 9, 23, 19, 58774), null=True, verbose_name='Last update time'),
        ),
    ]
