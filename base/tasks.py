import coreapi
from celery import shared_task
from django.conf import settings

from base.models import Submit


@shared_task(bind=True, queue='compile_queue')
def compile_code(self, submit_id):
    pass

def get_reports():
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    print(schema)
    reports=client.action(schema,['run','report','list'],params={'time':0})
    print(reports)
    for report in reports:
        submit=Submit.objects.get(run_id=report['id'])
        #print(report['parameters']['code_log'])
        #log = client.action(schema,['storage','get_file','read'],params={'token':report['parameters']['code_log']})
        #print(log)
        if(report['status']==2):
            submit.status=3
        else:
            submit.status=4
        submit.save()
