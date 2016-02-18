from django.core.management.base import BaseCommand
from base.tasks import compile_code
from base.models import Submit


class Command(BaseCommand):

    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('submit_info', nargs='+', type=str)
        parser.add_argument("--competition", nargs=1, type=int)
        parser.add_argument("--language_id", nargs=1, type=int)
        parser.add_argument("--status", nargs=1, type=int)
        parser.add_argument("--min_ID", nargs=1, type=int)

    def handle(self, *args, **options):

        if options["submit_info"][0] == "all":
            submission_list = Submit.objects.all().order_by('id')
        else:
            ids = [int(submit_id) for submit_id in options["submit_info"]]
            submission_list = Submit.objects.filter(pk__in=ids).order_by('id')

        if options.get("competition", None) is not None:
            submission_list = submission_list.filter(team__competition=options["competition"][0])

        if options.get("language_id", None) is not None:
            submission_list = submission_list.filter(lang__id=options["language_id"][0])

        if options.get("status", None) is not None:
            submission_list = submission_list.filter(status=options["status"][0])

        if options.get("min_ID", None) is not None:
            submission_list = submission_list.filter(id__gte=options["min_ID"][0])

        for submission in submission_list:
            print("Scheduling recompile of submission " + str(submission.id))
            compile_code.delay(submission.id)

