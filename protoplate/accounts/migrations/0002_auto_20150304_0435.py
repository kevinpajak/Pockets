# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bespokeuser',
            name='first_name',
            field=models.CharField(max_length=32, verbose_name='first name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bespokeuser',
            name='is_active',
            field=models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bespokeuser',
            name='last_name',
            field=models.CharField(max_length=32, verbose_name='last name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bespokeuser',
            name='picture',
            field=models.ImageField(upload_to='rofile_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bespokeuser',
            name='username',
            field=models.CharField(unique=True, max_length=32, help_text='Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')]),
            preserve_default=True,
        ),
    ]
