from django.core.management.base import BaseCommand
from django.core.files import File
from base.models import Submit, team_code_directory_path
from django.conf import settings


class Command(BaseCommand):

    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument("--competition", nargs=1, type=int)

    def handle(self, *args, **options):

        submission_list = Submit.objects.all()

        if options.get("competition", None) is not None:
            submission_list = submission_list.filter(team__competition=options["competition"])

        for submission in submission_list:
            try:
                #print(submission.code)
                current_file = settings.OLD_BASE_AND_GAME_STORAGE.open(submission.code)
                submission.code = settings.BASE_AND_GAME_STORAGE.save(
                    team_code_directory_path(submission, 'fake_name'), current_file)
                submission.save()
            except IOError:
                pass

