# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oil', models.IntegerField(default=750, verbose_name='Oil')),
                ('iron', models.IntegerField(default=750, verbose_name='Iron')),
                ('wood', models.IntegerField(default=750, verbose_name='Wood')),
                ('food', models.IntegerField(default=750, verbose_name='Food')),
            ],
        ),
        migrations.CreateModel(
            name='Troops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('research_time', models.TimeField()),
                ('training_time', models.TimeField()),
                ('description', models.TextField(max_length=2550)),
                ('research_cost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='troops.Resources')),
                ('training_cost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_cost', to='troops.Resources')),
                ('troop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Troop')),
            ],
        ),
    ]