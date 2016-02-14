from django.core.management import BaseCommand
from game.tasks import run_game

__author__ = 'hadi'

class Command(BaseCommand):
    def handle(self, *args, **ops):
        self.stdout.write("running...\n")
        run_game(1)
        self.stdout.write("finished!\n")
