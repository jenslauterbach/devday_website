# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-09-20 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0025_validatedimagefield_for_speaker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('name', 'event')]),
        ),
    ]
