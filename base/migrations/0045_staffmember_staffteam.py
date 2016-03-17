# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_auto_20160301_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='full name')),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('entrance_year', models.PositiveIntegerField(verbose_name='entrance year')),
                ('label', models.CharField(max_length=150, verbose_name='label', blank=True)),
                ('bio', models.CharField(max_length=300, verbose_name='biography', blank=True)),
                ('image', models.ImageField(upload_to=b'staff/images/', storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), verbose_name='image')),
            ],
            options={
                'verbose_name': 'staff member',
                'verbose_name_plural': 'staff',
            },
        ),
        migrations.CreateModel(
            name='StaffTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='team name')),
                ('members', models.ManyToManyField(to='base.StaffMember', verbose_name='team members', blank=True)),
                ('parent', models.ForeignKey(verbose_name='parent team', blank=True, to='base.StaffTeam', null=True)),
            ],
            options={
                'verbose_name': 'staff team',
                'verbose_name_plural': 'staff teams',
            },
        ),
    ]
