# -*- coding: utf-8 -*-
from __future__ import absolute_import

import celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIC_site.settings')


app = celery.Celery('AIC')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
