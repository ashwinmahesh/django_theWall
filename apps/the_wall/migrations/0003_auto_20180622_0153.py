# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-22 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_wall', '0002_auto_20180622_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]