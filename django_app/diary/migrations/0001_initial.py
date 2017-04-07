# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 00:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
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
            name='postphoto',
            order_with_respect_to='post',
        ),
        migrations.AlterOrderWithRespectTo(
            name='post',
            order_with_respect_to='diary',
        ),
    ]