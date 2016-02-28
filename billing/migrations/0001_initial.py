# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=1, choices=[(b'u', b'unknown'), (b'v', b'valid'), (b'c', b'cancelled')])),
                ('our_id', models.CharField(max_length=100)),
                ('order_id', models.CharField(max_length=100, null=True, blank=True)),
                ('bank', models.CharField(max_length=1, choices=[(b'2', b'tejarat'), (b'1', b'mellat')])),
                ('reference_id', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
