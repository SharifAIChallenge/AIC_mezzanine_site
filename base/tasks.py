# import os
#
import os

import coreapi
from celery import shared_task
import datetime

from decimal import Decimal
from django.conf import settings
from django.core.files.base import ContentFile

from base.models import Submit, LastGetReportsTime
from django.db import models
import json

from game.tasks import run_game

from game.models import Game, GameTeamSubmit


@shared_task
def get_reports():
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    reports=client.action(schema,['run','report','list'],params={'time':int(LastGetReportsTime.get_solo().time)-5000})
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
            try:
                game=Game.objects.get(run_id=report['id'])
            except Exception as exception:
                continue
            if(report['status']==2):
                logfile = client.action(schema, ['storage', 'get_file', 'read'],
                                        params={'token': report['parameters']['game_log']})
                if (logfile is None):
                    continue

                submissions = list(GameTeamSubmit.objects.all().filter(game=game).order_by('pk'))
                submissions[0].score,submissions[1].score = json.load(client.action(schema, ['storage', 'get_file', 'read'],
                                        params={'token': report['parameters']['game_score']}))
                submissions[0].save()
                submissions[1].save()
                game.log=logfile.read()
                game.log_file.save(report['parameters']['game_log'], ContentFile(game.log))
                game.status=3
            elif(report['status']==3):
                game.status=4
                pass
                #run_game.delay(game.id)
            game.save()

    instance=LastGetReportsTime.objects.get()
    instance.time=(datetime.datetime.utcnow()-datetime.datetime(1970,1,1)).total_seconds()
    instance.save()

