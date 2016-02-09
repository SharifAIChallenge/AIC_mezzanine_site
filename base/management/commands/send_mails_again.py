# -*- coding: utf-8 -*-
from base.models import Member
from django.contrib.auth.tokens import default_token_generator
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from mezzanine.conf import settings
from mezzanine.utils.email import subject_template, send_mail_template

from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **ops):
        count = 0
        verification_type = "signup_verify"
        request = {'get_host': 'aichallenge.sharif.edu:2016'}
        for user in tqdm(Member.objects.filter(is_active=False), leave=False):
            verify_url = reverse(verification_type, kwargs={
                "uidb36": int_to_base36(user.id),
                "token": default_token_generator.make_token(user),
            }) + "?next=" + "/"
            context = {
                "request": request,
                "user": user,
                "verify_url": verify_url,
            }
            subject_template_name = "email/%s_subject.txt" % verification_type
            subject = subject_template(subject_template_name, context)
            send_mail_template(subject, "email/%s" % verification_type,
                               settings.DEFAULT_FROM_EMAIL, user.email,
                               context=context)
            count += 1
        self.stdout.write("resent %d verification email" % count)
