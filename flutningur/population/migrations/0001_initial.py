# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Changes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('mid', models.IntegerField()),
                ('name', models.CharField(max_length=200, unique=True)),
                ('change', models.ManyToManyField(to='population.Municipality', through='population.Changes')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('year', models.IntegerField()),
                ('val', models.IntegerField(null=True)),
                ('municipality', models.ForeignKey(to='population.Municipality')),
            ],
        ),
        migrations.AddField(
            model_name='changes',
            name='new',
            field=models.ForeignKey(to='population.Municipality', related_name='municipality_new'),
        ),
        migrations.AddField(
            model_name='changes',
            name='old',
            field=models.ForeignKey(to='population.Municipality', related_name='municipality_old'),
        ),
    ]
