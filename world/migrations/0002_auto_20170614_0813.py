# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 08:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='food_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 145091), verbose_name='Food bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='iron_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 145005), verbose_name='Iron bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='oil_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 144959), verbose_name='Oil bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='plus_account',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 144900), verbose_name='Plus Account'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='wood_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 145049), verbose_name='Wood bonus production'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 152855)),
        ),
        migrations.AlterField(
            model_name='queue',
            name='next_update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 132001)),
        ),
        migrations.AlterField(
            model_name='village',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 8, 13, 36, 140611), null=True, verbose_name='Last update time'),
        ),
    ]