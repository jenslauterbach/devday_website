# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-01 19:28
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def create_default_slug(apps, schema_manager):
    Talk = apps.get_model('talk', 'Talk')
    for talk in Talk.objects.all():
        talk.slug = slugify(talk.title)
        talk.save()


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0027_talkformats'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='slug',
            field=models.SlugField(default='', verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.RunPython(create_default_slug)
    ]
