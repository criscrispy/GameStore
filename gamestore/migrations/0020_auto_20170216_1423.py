# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0019_auto_20170211_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.ForeignKey(default='misc', on_delete=django.db.models.deletion.CASCADE, to='gamestore.Category'),
        ),
    ]
