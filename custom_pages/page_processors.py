from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.email import send_mail_template
from .forms import AskedQuestionForm

from .models import QAPage, AskedQuestion


@processor_for(QAPage)
def question_and_answer_page_processor(request, page):
    if request.method == 'POST':
        url = page.get_absolute_url() + "?sent=1"

        question_form = AskedQuestionForm(data=request.POST)
        question = question_form.save(page.qapage, request.user)

        fields = [('questioner', question.questioner), ('question', question.question)]
        print(fields)
        send_mail_template(page.title, 'email/form_response', None, page.qapage.responder_mail,
                           context={'message': _('A new question is waiting for you!'), 'fields': fields})

        return redirect(url)


    question_form = AskedQuestionForm()
    return {'form': question_form}

