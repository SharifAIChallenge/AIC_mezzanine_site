# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_auto_20160317_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffmember',
            old_name='label',
            new_name='role',
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='image',
            field=models.ImageField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'staff/images/', null=True, verbose_name='image'),
        ),
    ]
