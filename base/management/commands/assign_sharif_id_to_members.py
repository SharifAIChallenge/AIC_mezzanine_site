from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
settings.SITE_ID=3
from base.models import SharifID, Member

class Command(BaseCommand):
    help = 'Assign every finilized members a Sharif ID'

    def handle(self, *args, **options):
        shids = list(SharifID.objects.all())
        shid_count = 0
        for mem in Member.objects.all():
            if mem.team and mem.team.will_come==0 and mem.team.timestamp.year==2017:
                for sh in mem.sharifid_set.all():
	            mem.sharifid_set.remove(sh)
                mem.sharifid_set.add(shids[shid_count])
                if shids[shid_count].member and shids[shid_count].member.username == mem.username:
                    self.stdout.write(self.style.ERROR(mem.username))
		self.stdout.write(self.style.WARNING(mem.team.name + ': ' + mem.username + ': ' + str(shids[shid_count])))
                shid_count += 1

        self.stdout.write(self.style.WARNING('%d members assigned to their Sharif IDs' % shid_count))
