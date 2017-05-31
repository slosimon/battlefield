# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 10:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Parliament', 'Parliament'), ('Summer residence', 'Summer residence'), ('Town hall', 'Town hall'), ('Headquarters', 'Headquarters'), ('Shelter', 'Shelter'), ('Warehouse', 'Warehouse'), ('Silo', 'Silo'), ('University', 'University'), ('Market', 'Market'), ('Training camp', 'Training camp'), ('Ammunition workshop', 'Ammunition workshop'), ('Hangar', 'Hangar'), ('Railway', 'Railway'), ('Port', 'Port'), ('Artilery mansion', 'Artilery mansion'), ("Hero's birth house", "Hero's birth house"), ('Hideout', 'Hideout'), ('Large warehouse', 'Large warehouse'), ('Large silo', 'Large silo'), ('Large camp', 'Large camp'), ('Large hangar', 'Large hangar'), ('Bunker', 'Bunker'), ('Defensive line', 'Defensive line'), ('Oil refinery', 'Oil refinery'), ('Iron works', 'Iron works'), ('Powerplant', 'Powerplant'), ('Slaughter house', 'Slaughter house'), ('Can filling centre', 'Can filling centre'), ('Nuke research lab', 'Nuke research lab')], max_length=50)),
                ('image', models.ImageField(upload_to=b'')),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('oil', models.IntegerField()),
                ('iron', models.IntegerField()),
                ('coal', models.IntegerField()),
                ('food', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('culture_points', models.IntegerField()),
                ('bonus', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='cost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.Cost'),
        ),
    ]