# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parte',
            name='validacoes',
        ),
        migrations.AddField(
            model_name='validacao',
            name='parte',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='part.Parte'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alerta',
            name='data_alerta',
            field=models.DateField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='nivelautorizacao',
            name='nivel',
            field=models.CharField(choices=[('superior', 'SUPERIOR'), ('subcomando', 'SUBCOMANDO'), ('comando', 'COMANDO')], max_length=20),
        ),
        migrations.AlterField(
            model_name='parte',
            name='upload',
            field=models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='Anexo'),
        ),
        migrations.AlterField(
            model_name='tipoparte',
            name='alerta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='part.Alerta'),
        ),
        migrations.AlterField(
            model_name='tipoparte',
            name='tpDescricao',
            field=models.CharField(max_length=200, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='tipoparte',
            name='tpModelo',
            field=models.TextField(verbose_name='Modelo'),
        ),
    ]
