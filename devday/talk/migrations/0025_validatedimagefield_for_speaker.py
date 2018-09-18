# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-09-18 13:32
from __future__ import unicode_literals

import devday.extras
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0024_talkmedia_codelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='portrait',
            field=devday.extras.ValidatedImageField(upload_to='speakers', verbose_name='Speaker image'),
        ),
    ]
