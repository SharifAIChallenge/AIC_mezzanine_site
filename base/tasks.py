# import os
#
import os

import coreapi
from celery import shared_task
from django.conf import settings
from base.models import Submit
import json


@shared_task
def get_reports():
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    reports=client.action(schema,['run','report','list'],params={'time':0})
    for report in reports:
        if(len(Submit.objects.filter(run_id=report['id']))>0):
            submit=Submit.objects.get(run_id=report['id'])
        if(report['status']==2):
            submit.compiled_id=report['parameters']['code_compiled_zip']
            if(submit.status!=3):
                log = json.loads(client.action(schema, ['storage', 'get_file', 'read'],
                params={'token': report['parameters']['code_log']}).read())
                if len(log["errors"]) == 0:
                    submit.status = 3
                else:
                    submit.status = 4
                    submit.compile_log_file = '\n'.join(error for error in log["errors"])
        submit.save()
