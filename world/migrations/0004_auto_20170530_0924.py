# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 09:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20170528_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ally_leadership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=50)),
                ('mm_rights', models.BooleanField()),
                ('diplomacy', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Medals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField()),
                ('week', models.IntegerField()),
                ('medal', models.CharField(choices=[('Attack', '%d. attacker of the week %d'), ('Defense', '%d. defender of the week  %d'), ('Raiding', '%d. robber of the week %d'), ('Climber', '%d. climber of the week %d')], max_length=10)),
                ('image', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='alliance',
            name='old_population',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='activation_key',
            field=models.CharField(default='sad', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='attack_points',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='def_points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='last_village',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='last', to='world.Village'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='old_att',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='old_def',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='old_rank',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='raided',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bonus',
            name='coal_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 449093), verbose_name='Coal bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='food_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 449135), verbose_name='Food bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='iron_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 449051), verbose_name='Iron bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='oil_bonus_production',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 449004), verbose_name='Oil bonus production'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='plus_account',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 448944), verbose_name='Plus Account'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 456665)),
        ),
        migrations.AlterField(
            model_name='village',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 9, 23, 56, 445793), verbose_name='Last update time'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='ally',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Alliance'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='invited',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Player'),
        ),
        migrations.AddField(
            model_name='ally_leadership',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Player'),
        ),
        migrations.AddField(
            model_name='alliance',
            name='leadership',
            field=models.ManyToManyField(to='world.Ally_leadership'),
        ),
        migrations.AddField(
            model_name='alliance',
            name='medals',
            field=models.ManyToManyField(to='world.Medals'),
        ),
        migrations.AddField(
            model_name='player',
            name='medals',
            field=models.ManyToManyField(to='world.Medals'),
        ),
    ]
