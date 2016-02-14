import os
import random
import shutil
import zipfile
from string import ascii_lowercase as lowers

from celery import shared_task

from game.models import Game


@shared_task(bind=True, queue='game_queue')
def run_game(self, game_id):
    try:
        run_game_unsafe(game_id)
    except:
        self.retry()

def run_game_unsafe(game_id):
    game = Game.objects.get(id=game_id)

    competition_dir = '/competitions/' + str(game.competition.id)
    game_dir = competition_dir + '/' + str(game.id)

    # prepare yaml context
    game_clients = [
        {
            'id': submit.id,
            'name': submit.team.name,
            'lang': submit.pl,
            'token': generate_random_token(),
            'root': game_dir + '/clients/' + str(submit.id),
            'compile_result': submit.compile_result,
            'container': submit.lang.execute_container.get_image_id(),
        }
        for submit in game.players.all()
    ]
    game_ui = {
        'port': 7000,
        'token': generate_random_token(),
    }
    game_server = {
        'client_port': 7099,
        'root': game_dir + '/server' + str(game.competition.server_version),
        'compiled_code': game.competition.server.compiled_code,
        'container': game.competition.server.execute_container,
    }
    game_additional_containers = {
        container.tag: container.get_image_id() for container in game.competition.additional_containers.all()
    }
    game_context = {
        'server': game_server,
        'clients': game_clients,
        'ui': game_ui,
        'additional_containers': game_additional_containers,
    }

    # prepare game files
    make_dir(game_dir)

    # extract server (check if server exists)
    if not os.path.exists(game_server['root']):
        extract_zip(game_server['code'], game_server['root'])

    # extract compile result
    for client in game_clients:
        extract_zip(client['code'], client['root'])


def generate_random_token(length=32):
    return ''.join([lowers[random.randrange(0, len(lowers))] for i in range(length)])


def make_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def extract_zip(file_field, dst):
    make_dir(dst)
    with file_field.open('r') as fs:
        zf = zipfile.ZipFile(fs)
        zf.extractall(dst)
