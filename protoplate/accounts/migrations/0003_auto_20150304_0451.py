# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150304_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bespokeuser',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_images'),
            preserve_default=True,
        ),
    ]
