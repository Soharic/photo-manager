# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-27 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0007_auto_20181227_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='phototag',
            name='significance',
            field=models.FloatField(null=True),
        ),
    ]
