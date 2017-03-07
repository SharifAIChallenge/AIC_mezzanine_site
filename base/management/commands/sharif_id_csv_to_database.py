from django.core.management.base import BaseCommand, CommandError
from base.models import SharifID
import csv

class Command(BaseCommand):
    help = 'Writes a given CVS file of Sharif IDs into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        SharifID.objects.all().delete()
        for filename in options['filename']:
            with open(filename, 'r') as csvfile:
                shidreader = csv.reader(csvfile, delimiter=',', quotechar='\n')
                for row in shidreader:
                    shid = SharifID(username=row[0], password=row[1])
                    shid.save()

        count = SharifID.objects.count()
        self.stdout.write(self.style.WARNING('%d Sharif IDs got into the database' % count))
