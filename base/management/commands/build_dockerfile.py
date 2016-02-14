from django.core.management import BaseCommand
from game.models import DockerContainer

__author__ = 'hadi'

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise AssertionError('Must pass exactly one parameter.')
        docker_id = int(args[0])
        docker = DockerContainer.objects.get(id=docker_id)
        self.stdout.write('building...\n')
        image_id = docker.get_image_id()
        self.stdout.write('build log:\n')
        self.stdout.write(docker.build_log)
        self.stdout.write("finished, image id: %s\n" % image_id)
