# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hero_experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('experience', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Hero_revive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oil', models.IntegerField(default=750, verbose_name='Oil')),
                ('iron', models.IntegerField(default=750, verbose_name='Iron')),
                ('coal', models.IntegerField(default=750, verbose_name='Coal')),
                ('food', models.IntegerField(default=750, verbose_name='Food')),
            ],
        ),
        migrations.AddField(
            model_name='hero_revive',
            name='cost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hero.Resources'),
        ),
    ]