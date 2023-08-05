# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 21:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(db_index=True, max_length=255)),
                ('task_params', models.TextField()),
                ('task_hash', models.CharField(db_index=True, max_length=40)),
                ('verbose_name', models.CharField(blank=True, max_length=255, null=True)),
                ('priority', models.IntegerField(db_index=True, default=0)),
                ('run_at', models.DateTimeField(db_index=True)),
                ('repeat', models.BigIntegerField(choices=[(3600, 'hourly'), (86400, 'daily'), (604800, 'weekly'), (1209600, 'every 2 weeks'), (2419200, 'every 4 weeks'), (0, 'never')], default=0)),
                ('repeat_until', models.DateTimeField(blank=True, null=True)),
                ('queue', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('attempts', models.IntegerField(db_index=True, default=0)),
                ('failed_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('last_error', models.TextField(blank=True)),
                ('locked_by', models.CharField(blank=True, db_index=True, max_length=64, null=True)),
                ('locked_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('creator_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('creator_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completed_background_task', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(db_index=True, max_length=255)),
                ('task_params', models.TextField()),
                ('task_hash', models.CharField(db_index=True, max_length=40)),
                ('verbose_name', models.CharField(blank=True, max_length=255, null=True)),
                ('priority', models.IntegerField(db_index=True, default=0)),
                ('run_at', models.DateTimeField(db_index=True)),
                ('repeat', models.BigIntegerField(choices=[(3600, 'hourly'), (86400, 'daily'), (604800, 'weekly'), (1209600, 'every 2 weeks'), (2419200, 'every 4 weeks'), (0, 'never')], default=0)),
                ('repeat_until', models.DateTimeField(blank=True, null=True)),
                ('queue', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('attempts', models.IntegerField(db_index=True, default=0)),
                ('failed_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('last_error', models.TextField(blank=True)),
                ('locked_by', models.CharField(blank=True, db_index=True, max_length=64, null=True)),
                ('locked_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('creator_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('creator_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='background_task', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'background_task',
            },
        ),
    ]
