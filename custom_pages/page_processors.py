from django.utils.translation import ugettext as _
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.email import split_addresses, send_mail_template
from .forms import AskedQuestionForm

from .models import QAPage, AskedQuestion


@processor_for(QAPage)
def question_and_answer_page_processor(request, page):
    if request.method == 'POST':
        question_form = AskedQuestionForm(data=request.POST)
        question_form.save(page.qapage, request.user)

    question_form = AskedQuestionForm()
    return {'form': question_form}

