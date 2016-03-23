# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 18:54
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webinterface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Analyses',
                'verbose_name': 'Analysis',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turbine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('manufacturer', models.CharField(blank=True, max_length=300, null=True)),
                ('model', models.CharField(blank=True, max_length=300, null=True)),
                ('hubHeight', models.FloatField(default=80)),
                ('diameter', models.FloatField(default=90)),
                ('bin', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, null=True, size=None)),
                ('powerInKillowats', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, null=True, size=None)),
                ('stripes', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='turbine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='turbine', to='webinterface.Turbine'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webinterface.Project'),
        ),
    ]