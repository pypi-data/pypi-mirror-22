# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-04-10 04:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lorikeet', '0013_auto_20170307_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='purchased_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
