# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150412_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='state',
            new_name='is_seen',
        ),
        migrations.AddField(
            model_name='message',
            name='is_seen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
