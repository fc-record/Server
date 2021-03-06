# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 15:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default='2017-04-14 00:02')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('diary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.Diary')),
            ],
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='post')),
                ('gpsLatitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('gpsLongitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.Post')),
            ],
        ),
        migrations.AlterOrderWithRespectTo(
            name='post',
            order_with_respect_to='created_date',
        ),
    ]
