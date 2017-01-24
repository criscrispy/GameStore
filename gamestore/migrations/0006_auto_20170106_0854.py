# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0005_auto_20170104_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='developer_status',
            field=models.CharField(choices=[('0', 'basic_user'), ('1', 'pending'), ('2', 'confirmed')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='gamesale',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date when game was bought'),
        ),
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=''),
        ),
    ]