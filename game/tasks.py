import json
import uuid

import coreapi
from celery import shared_task
from django.conf import settings

#from game.models import Game
from game.models import Game
from game.models import GameTeamSubmit


@shared_task
def run_game(game_id):
    credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    game = Game.objects.get(pk=game_id)
    ans = client.action(schema, ['storage', 'new_file', 'update'],
                        params={'file': coreapi.utils.File(name='file',content=game.game_config.config)})
    # game.token;
    # game.token = ans['token']
    submissions = list(GameTeamSubmit.objects.all().filter(game=game).order_by('pk'))
    if len(submissions) != 2:
        raise ValueError()
    ans = client.action(schema, ['run', 'run', 'create'], params={
        'data':[{'operation': 'execute', 'parameters': {
            "client1_id": submissions[0].pk,
            "client1_token": str(uuid.uuid4()),
            "client1_code": submissions[0].submit.compiled_id,
            "client2_id": submissions[1].pk,
            "client2_token": str(uuid.uuid4()),
            "client2_code": submissions[1].submit.compiled_id,
            "logger_token": str(uuid.uuid4()),
            "server_game_config": ans['token'],
        }}]})
    game.run_id = ans[0]['run_id']
    game.save()