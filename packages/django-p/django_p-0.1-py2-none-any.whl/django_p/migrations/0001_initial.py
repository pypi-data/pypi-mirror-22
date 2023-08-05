# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-29 09:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barrier',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('triggered', models.DateTimeField()),
                ('status', models.IntegerField(choices=[
                 (1, b'FIRED'), (0, b'WAITING')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('class_path', models.CharField(max_length=255)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('finalized', models.DateTimeField(auto_now=True)),
                ('params', jsonfield.fields.JSONField(default={})),
                ('status', models.IntegerField(choices=[
                 (3, b'WAITING'), (2, b'RUN'), (1, b'DONE'), (0, b'ABORTED')], default=3)),
                ('current_attempt', models.IntegerField(default=0)),
                ('max_attempts', models.IntegerField(default=1)),
                ('next_retry_time', models.DateTimeField()),
                ('retry_message', models.TextField()),
                ('abort_message', models.TextField()),
                ('abort_requested', models.BooleanField(default=False)),
                ('parent_pipeline', models.ForeignKey(blank=True, null=True,
                                                      on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_p.Pipeline')),
                ('root_pipeline', models.ForeignKey(blank=True, null=True,
                                                    on_delete=django.db.models.deletion.CASCADE, related_name='descendants', to='django_p.Pipeline')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', jsonfield.fields.JSONField(default={})),
                ('status', models.IntegerField(choices=[
                 (1, b'FILLED'), (0, b'WAITING')], default=0)),
                ('filled', models.DateTimeField(auto_now=True)),
                ('filler', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='django_p.Pipeline')),
            ],
        ),
        migrations.AddField(
            model_name='barrier',
            name='blocking_slots',
            field=models.ManyToManyField(to='django_p.Slot'),
        ),
        migrations.AddField(
            model_name='barrier',
            name='target',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='django_p.Pipeline'),
        ),
        migrations.AlterUniqueTogether(
            name='slot',
            unique_together=set([('filler', 'name')]),
        ),
    ]
