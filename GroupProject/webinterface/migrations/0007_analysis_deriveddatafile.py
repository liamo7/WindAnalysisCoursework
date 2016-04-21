# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-16 08:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0006_auto_20160414_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='derivedDataFile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='derivedDataFile', to='webinterface.JsonDataFile'),
        ),
    ]