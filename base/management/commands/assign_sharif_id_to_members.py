from django.core.management.base import BaseCommand, CommandError
from base.models import SharifID, Member

class Command(BaseCommand):
    help = 'Assign every finilized members a Sharif ID'

    def handle(self, *args, **options):
        shids = SharifID.objects.all()
        shid_count = 0
        for mem in Member.objects.all():
            if mem.team and mem.team.has_paid:
                for sh in mem.sharifid_set.all():
	                mem.sharifid_set.remove(sh)
                mem.sharifid_set.add(shids[shid_count])
                shid_count += 1

        self.stdout.write(self.style.WARNING('%d members assigned to their Sharif IDs' % shid_count))