# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 19:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_projects', '0031_project_hidden_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('unapplied', 'Canceled')], default='applied', max_length=30, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='volunteerrole',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='ovp_projects.Project', verbose_name='Project'),
        ),
    ]
