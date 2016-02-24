# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 13:46
from __future__ import unicode_literals

from django.db import migrations, models
import webinterface.models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='site_calibration_file',
            field=models.FileField(upload_to=webinterface.models.ProjectManager.getUploadPath),
        ),
    ]
