# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0002_jsondatafile_projectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='combinedDataFile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='combinedDataFile', to='webinterface.JsonDataFile'),
        ),
    ]
