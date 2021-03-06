# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-26 08:52
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0017_speaker_public_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalkMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube', models.CharField(max_length=64, verbose_name='Youtube video id')),
                ('slideshare', models.CharField(max_length=64, verbose_name='Slideshare id')),
                ('talk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='talk.Talk')),
            ],
        ),
    ]
