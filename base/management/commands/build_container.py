from django.core.management import BaseCommand
from game.models import DockerContainer

__author__ = 'hadi'

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('docker_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for docker_id in options['docker_id']:
            docker = DockerContainer.objects.get(id=int(docker_id))
            self.stdout.write('building...\n')
            image_id = docker.get_image_id()
            self.stdout.write('build log:\n')
            self.stdout.write(docker.build_log)
            self.stdout.write("finished, image id: %s\n" % image_id)
