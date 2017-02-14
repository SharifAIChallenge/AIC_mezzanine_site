# import os
#
import os

import coreapi
import celery
from celery import Celery
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
# from django.conf import settings
#from AIC_site import _celery
# #from AIC_SITE._celery import app
#
# from base.models import Submit
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIC_site.settings')
# app = Celery('AIC')
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)





#@periodic_task(run_every=crontab(hour="*", minute="0", day_of_week="*"), ignore_result=True)
#from base.models import Submit
from django.conf import settings

from base.models import Submit


@shared_task
def get_reports():
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    reports=client.action(schema,['run','report','list'],params={'time':0})
    print(reports)
    for report in reports:
        submit=Submit.objects.get(run_id=report['id'])


        if(report['status']==2):
            submit.compiled_id=report['parameters']['code_compiled_zip']
            if(submit.status!=3):
                log = client.action(schema, ['storage', 'get_file', 'read'],
                params={'token': report['parameters']['code_log']})
                if log is None:
                    log = {"errors": []}
                print(log)
                if len(log["errors"]) == 0:
                    submit.status = 3
                else:
                    submit.status = 4
                    submit.compile_log_file = str(log["errors"])
        submit.save()
