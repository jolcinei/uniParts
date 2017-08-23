# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0002_auto_20170809_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='lido',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='parte',
            name='qtd_validacoes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parte',
            name='status',
            field=models.CharField(choices=[('NOVA', 'NOVA'), ('AUTORIZADO', 'AUTORIZADO'), ('EM_ANALISE', 'EM ANALISE'), ('NEGADO', 'NEGADO'), ('PUBLICADO', 'PUBLICADO')], default=1, max_length=32),
            preserve_default=False,
        ),
    ]
