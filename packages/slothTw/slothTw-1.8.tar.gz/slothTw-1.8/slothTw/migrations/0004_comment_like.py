# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-01 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slothTw', '0003_comment_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
