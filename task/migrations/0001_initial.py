# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1024)),
                ('date_published', models.DateField()),
                ('owner', models.ForeignKey(to='task.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('date_published', models.DateField()),
                ('state', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to='task.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_published', models.DateField()),
                ('date_due', models.DateField()),
                ('state', models.BooleanField()),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('owner', models.ForeignKey(to='task.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='task',
            field=models.ForeignKey(to='task.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='task',
            field=models.ForeignKey(to='task.Task'),
            preserve_default=True,
        ),
    ]
