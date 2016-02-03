from django.db import models
from mezzanine.core.models import Orderable
from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page, RichText
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape

class ContainerPage(Page):
    pass

    class Meta:
        verbose_name = _("Container Page")
        verbose_name_plural = _("Container Pages")


class QAPage(Page, RichText):
    responder_mail = models.EmailField(max_length=2014, null=True, blank=True, verbose_name=_("Responder Mail"))

    class Meta:
        verbose_name = _("QA Page")
        verbose_name_plural = _("QA Pages")


class AskedQuestion(Orderable):
    page = models.ForeignKey(QAPage, verbose_name=_("Containing Page"))
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Time"))
    questioner = models.ForeignKey('base.Member', null=False, verbose_name=_("Questioner"))
    question = models.CharField(max_length=1024, null=False, blank=False,
                                verbose_name=_("Question"), help_text=_('Ask New Question'))
    answer = RichTextField(null=True, blank=True, verbose_name=_("Answer"))
    is_approved = models.BooleanField(default=True, verbose_name=_("Approved"))

    def question_head(self):
        if len(self.question) > 128:
            return escape(self.question)[:128] + "..."
        return escape(self.question)

    question_head.allow_tags = True
    question_head.short_description = _("Question")

    def answer_head(self):
        if self.answer is None:
            return 'No Answer'
        if len(self.answer) > 128:
            return escape(self.answer)[:128] + "..."
        return escape(self.answer)

    answer_head.allow_tags = True
    answer_head.short_description = _("Answer")

    class Meta:
        verbose_name = _("Asked Question")
        verbose_name_plural = _("Asked Questions")

