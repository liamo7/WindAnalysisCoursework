# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0004_auto_20160410_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='siteCalibrationDict',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='siteCalibrationDict', to='webinterface.JsonDataFile'),
        ),
    ]
