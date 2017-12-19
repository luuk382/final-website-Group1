# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Vegan', 'Vegan'), ('Dessert', 'Dessert'), ('Quick', 'Quick'), ('Dinner', 'Dinner'), ('Soup', 'Soup'), ('Salad', 'Salad')], help_text='Please enter the category of your recipe. It will be displayed on All recipes page.', max_length=10, null=True),
        ),
    ]
