# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0003_auto_20170809_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parte',
            options={'ordering': ['author', 'descricao', 'tipoParte'], 'verbose_name': 'parte', 'verbose_name_plural': 'partes'},
        ),
        migrations.AddField(
            model_name='parte',
            name='boletim_interno',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parte',
            name='data_publicacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parte',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Anexo'),
        ),
    ]
