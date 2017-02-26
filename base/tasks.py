# import os
#
import os

import coreapi
from celery import shared_task
import datetime
from django.conf import settings
from base.models import Submit, LastGetReportsTime
import json

from game.tasks import run_game

from game.models import Game


@shared_task
def get_reports():
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    print(LastGetReportsTime.get_solo().time)
    reports=client.action(schema,['run','report','list'],params={'time':int(LastGetReportsTime.get_solo().time)-10})
    for report in reports:
        if(report['operation']=='compile'):
            if(len(Submit.objects.filter(run_id=report['id']))==0):
                continue
            submit=Submit.objects.get(run_id=report['id'])
            if(report['status']==2):
                submit.compiled_id=report['parameters']['code_compiled_zip']
                if(submit.status<3):
                    logfile=client.action(schema, ['storage', 'get_file','read'],
                    params={'token': report['parameters']['code_log']})
                    if(logfile is None):
                        continue
                    log = json.loads(logfile.read())
                    if len(log["errors"]) == 0:
                        submit.status = 3
                    else:
                        submit.status = 4
                        submit.compile_log_file = '\n'.join(error for error in log["errors"])
            elif(report['status']==3):
                submit.status=4
                submit.compile_log_file = 'Unknown error occurred maybe compilation timed out'
            submit.save()
        elif(report['operation']=='execute'):
            print(report)
            try:
                game=Game.objects.get(run_id=report['id'])
            except Exception:
                continue
            if(report['status']==2):
                logfile = client.action(schema, ['storage', 'get_file', 'read'],
                                        params={'token': report['parameters']['game_log']})
                if (logfile is None):
                    continue
                game.log=logfile.read()
            elif(report['status']==3):
                game.status=4
                pass
                #run_game.delay(game.id)
            game.save()

    instance=LastGetReportsTime.objects.get()
    instance.time=(datetime.datetime.utcnow()-datetime.datetime(1970,1,1)).total_seconds()
    instance.save()

