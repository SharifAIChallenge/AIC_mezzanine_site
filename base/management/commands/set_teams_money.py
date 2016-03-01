from django.core.management.base import BaseCommand
from base.models import Team
from django.db import transaction

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("teams_list_file", nargs=1, type=str)
        parser.add_argument("payment_value", nargs=1, type=int)

    def handle(self, *args, **options):
        with open(options["teams_list_file"][0]) as file:
            with transaction.atomic():
                for line in file.readlines():
                    try:
                        team = Team.objects.get(name=line.strip("\n"))
                        team.should_pay = True
                        team.payment_value = options["payment_value"][0]
                        team.save()
                    except:
                        print("Problem in settiing team's money: %s" % line)
                        raise Exception
