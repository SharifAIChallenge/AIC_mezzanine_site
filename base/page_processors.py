from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy
from mezzanine.pages.page_processors import processor_for


@processor_for('docs/competition')
def final_teams_only(request, page):
    team = request.user.team
    if not team or not team.final:
        messages.error(request, ugettext_lazy('your team must be final'))
        return redirect('my_team')
    return {"page": page}
