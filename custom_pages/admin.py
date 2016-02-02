from copy import deepcopy

from django.contrib import admin
from mezzanine.core import admin as mezzanineAdmin

from mezzanine.pages.admin import PageAdmin

from .models import ContainerPage, QAPage, AskedQuestion


class ContainerPageAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets)

admin.site.register(ContainerPage, ContainerPageAdmin)


question_and_answer_page_fieldsets = deepcopy(PageAdmin.fieldsets)
question_and_answer_page_fieldsets[0][1]["fields"].insert(+3, "content")
question_and_answer_page_fieldsets[0][1]["fields"].insert(+4, "responder_mail")


class AskedQuestionInline(mezzanineAdmin.StackedDynamicInlineAdmin):
    model = AskedQuestion


class QAPageAdmin(PageAdmin):
    inlines = (AskedQuestionInline,)
    fieldsets = question_and_answer_page_fieldsets

admin.site.register(QAPage, QAPageAdmin)


class AskedQuestionAdmin(mezzanineAdmin.BaseTranslationModelAdmin):
    fieldsets = ((None, {"fields": ("page", "is_approved", "questioner", "question", "answer")}),)
    list_display = ("page", "creation_time", "questioner", "question_head", "answer_head", "is_approved")
    list_display_links = ("creation_time", "questioner", "question_head", "answer_head")
    list_editable = ("page", "is_approved")
    list_filter = ("page", "questioner", "creation_time", "is_approved")
    search_fields = ("question", "answer")

admin.site.register(AskedQuestion, AskedQuestionAdmin)