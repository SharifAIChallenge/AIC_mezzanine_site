# import os
#
import os

import coreapi
from celery import Celery
from celery import shared_task
from celery.bin import celery
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

app = Celery('AIC')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIC_site.settings')

app.config_from_object('django.conf:settings')
@app.task
def khar():
    print("sag")

def get_reports():
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    reports=client.action(schema,['run','report','list'],params={'time':0})
    print(reports)
    for report in reports:
        submit=Submit.objects.get(run_id=report['id'])

        #log = client.action(schema,['storage','get_file','read'],params={'token':report['parameters']['code_log']})
        #print(log)
        if(report['status']==2):
            submit.compiled_id=report['parameters']['code_compiled_zip']
            if(submit.status!=3):
                print(report['parameters']['code_log'])
            submit.status=3
        submit.save()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'khar',
        'schedule': 30.0,
    },
}