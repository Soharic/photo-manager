# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-03 19:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20181114_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name']},
        ),
    ]
