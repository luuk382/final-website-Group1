# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-15 10:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_auto_20180114_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='author_user',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='post',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
