# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 19:30
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import enumfields.fields
import windAnalysis.ppaTypes


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0003_auto_20160323_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('columnType', enumfields.fields.EnumField(enum=windAnalysis.ppaTypes.ColumnType, max_length=10)),
                ('valueType', enumfields.fields.EnumField(enum=windAnalysis.ppaTypes.ValueType, max_length=10)),
                ('instrumentCalibrationSlope', models.FloatField(blank=True, default=1.0, null=True)),
                ('instrumentCalibrationOffset', models.FloatField(blank=True, default=0.0, null=True)),
                ('dataLoggerCalibrationSlope', models.FloatField(blank=True, default=1.0, null=True)),
                ('dataLoggerCalibrationOffset', models.FloatField(blank=True, default=0.0, null=True)),
                ('measurementHeight', models.FloatField(blank=True, default=0.0, null=True)),
                ('segmentWeighting', models.FloatField(blank=True, null=True)),
                ('inferiorLimitHeight', models.FloatField(blank=True, null=True)),
                ('superiorLimitHeight', models.FloatField(blank=True, null=True)),
                ('segmentHeight', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=500)),
                ('directory', models.CharField(max_length=500)),
                ('fileType', enumfields.fields.EnumField(enum=windAnalysis.ppaTypes.FileType, max_length=10)),
                ('columns', django.contrib.postgres.fields.jsonb.JSONField()),
                ('columnSeparator', models.CharField(max_length=10)),
                ('rowsToSkip', django.contrib.postgres.fields.jsonb.JSONField()),
                ('columnSets', django.contrib.postgres.fields.jsonb.JSONField()),
                ('badDataValues', django.contrib.postgres.fields.jsonb.JSONField()),
                ('selectors', django.contrib.postgres.fields.jsonb.JSONField()),
                ('rewsLevels', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
