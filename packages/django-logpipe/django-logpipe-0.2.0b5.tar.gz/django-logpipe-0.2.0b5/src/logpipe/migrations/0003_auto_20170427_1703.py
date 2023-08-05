# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logpipe', '0002_auto_20170427_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='KinesisOffset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream', models.CharField(help_text='The Kinesis stream name', max_length=200)),
                ('shard', models.CharField(help_text='The Kinesis shard ID', max_length=20)),
                ('sequence_number', models.CharField(help_text='The current sequence number in the Kinesis shard', max_length=20)),
            ],
            options={
                'ordering': ('stream', 'shard', 'sequence_number'),
            },
        ),
        migrations.AlterField(
            model_name='kafkaoffset',
            name='offset',
            field=models.PositiveIntegerField(default=0, help_text='The current offset in the Kafka partition'),
        ),
        migrations.AlterField(
            model_name='kafkaoffset',
            name='partition',
            field=models.PositiveIntegerField(help_text='The Kafka partition identifier'),
        ),
        migrations.AlterField(
            model_name='kafkaoffset',
            name='topic',
            field=models.CharField(help_text='The Kafka topic name', max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='kinesisoffset',
            unique_together=set([('stream', 'shard')]),
        ),
    ]
