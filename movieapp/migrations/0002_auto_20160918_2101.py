# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdbID', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=700)),
                ('year', models.CharField(max_length=100)),
                ('rated', models.CharField(max_length=100)),
                ('released', models.CharField(max_length=100)),
                ('runtime', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=250)),
                ('director', models.CharField(max_length=400)),
                ('writer', models.CharField(max_length=400)),
                ('actors', models.CharField(max_length=600)),
                ('plot', models.TextField()),
                ('language', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('poster', models.CharField(max_length=1000)),
                ('metascore', models.CharField(max_length=50)),
                ('imdbRating', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='familyName',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstName',
            field=models.CharField(max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='watchedList',
            field=models.ManyToManyField(to='movieapp.Movie'),
        ),
    ]