import coreapi
from celery import shared_task
from django.conf import settings

#from game.models import Game


@shared_task(bind=True, queue='game_queue')
def run_game(self, game_id):
    # credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
    # transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
    # client = coreapi.Client(transports=transports)
    # schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
    # ans = client.action(schema, ['storage', 'new_file', 'update'],
    #                     params={'file': coreapi.utils.File(name='file')})
    # game = Game.objects.get(pk=game_id)
    # game.token = ans['token']
    # ans = client.action(schema, ['run', 'run', 'create'], params={
    #     'data': [{'operation': 'execute', 'parameters': {
    #         "client1_id":game.players.__list__()[0],
    #         "client1_token":game.token,
    #         "client1_code":0,
    #         "client2_id":game.players.__list__()[1],
    #         "client2_token":0,
    #         "client2_code":0,
    #         "logger_token":"",
    #         "server_game_config":""
    #     }}]})
    # game.run_id = ans[0]['run_id']
    # game.save()
    pass
