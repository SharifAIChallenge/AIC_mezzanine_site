# -*- coding: utf-8 -*-
import json
from functools import wraps
from urlparse import urlparse

from base.forms import SubmitForm, TeamForm, InvitationForm, TeamNameForm, WillComeForm
from base.models import TeamInvitation, Team, Member, JoinRequest, Message, GameRequest, Submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import get_language_from_request
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from game.models import Competition, GameTeamSubmit
from mezzanine.utils.email import send_mail_template
from .tasks import compile_code


def registration_period_ended(request):
    competition = Competition.objects.get(site_id=request.site_id)
    return timezone.now() > competition.registration_finish_date


def team_required(function=None, register_period_only=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'team') and request.user.team:
                if register_period_only and registration_period_ended(request):
                    messages.error(request, _("registration period has ended"))
                    resolved_login_url = reverse('my_team')
                else:
                    request.team = request.user.team
                    return view_func(request, *args, **kwargs)
            else:
                messages.info(request,
                              _("you are not in a team, create one below or request your team leader to invite you"))
                resolved_login_url = reverse('register_team')
            path = request.build_absolute_uri()
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, 'next')

        return _wrapped_view

    if function:
        return decorator(function)
    return decorator


@login_required
def register_team(request):
    if registration_period_ended(request):
        messages.error(request, _("registration period has ended"))
        return redirect('teams_list')
    if request.user.team:
        return redirect('my_team')
    if request.method == 'POST':
        form = TeamForm(data=request.POST)
        if form.is_valid():
            team = form.save(user=request.user, competition=Competition.objects.get(site_id=request.site_id))
            request.session['team'] = team.id
            return redirect('invite_member')
    else:
        form = TeamForm()
    context = {'form': form, 'title': _('register new team')}

    invitation = TeamInvitation.objects.filter(member=request.user, accepted=False).select_related('team').all()[:1]
    is_invited = len(invitation) > 0
    context['is_invited'] = is_invited
    if is_invited:
        context['invitation'] = invitation[0]
    return render(request, 'accounts/invite_team.html', context)


@login_required
@team_required(register_period_only=True)
def invite_member(request):
    if request.user.id != request.team.head_id:
        messages.error(request, _("only head can invite"))
        return redirect('my_team')
    if request.method == 'POST':
        form = InvitationForm(data=request.POST)
        if form.is_valid():
            if form.member.team:
                if form.member.team == request.team:
                    messages.info(request, _("already part of the team"))
                else:
                    messages.error(request, _("already part of another team"))
            elif TeamInvitation.objects.filter(member=form.member, team=request.team).exists():
                messages.warning(request, _("you have invited this user before!"))
            else:
                form.save(team=request.team, host=request.get_host)
                messages.info(request, _("please check spams too"))
                messages.success(request,
                                 _('successfully invited user %(name)s') % {'name': form.member.get_full_name()})
                return redirect('invite_member')
    else:
        form = InvitationForm()
    return render(request, 'accounts/invite_team.html', {'form': form, 'title': _('invite member to team')})


@login_required
@team_required
def submit(request):
    competition = request.team.competition
    if not request.team.final:
        messages.error(request, _('your team must be final'))
        return redirect('my_team')
    if request.team.member_set.count() < request.team.competition.min_members:
        messages.error(request, _("your team does not have enough members"))
        return redirect('invite_member')
    if request.method == 'POST':
        form = SubmitForm(competition, data=request.POST, files=request.FILES)
        if form.is_valid():
            new_submit = form.save(commit=False)
            new_submit.team = request.team
            new_submit.submitter = request.user
            new_submit.save()
            compile_code.delay(new_submit.id)
            return redirect('submit_code')
    else:
        form = SubmitForm(competition)
    return render(request, 'accounts/submit_code.html', {
        'form': form,
        'title': _('submit new code'),
        'submissions': Submit.objects.filter(team=request.team).order_by('-timestamp').all()
    })


@login_required
def accept_invite(request, slug):
    if registration_period_ended(request):
        messages.error(request, _("registration period has ended"))
        return redirect('teams_list')
    try:
        invitation = TeamInvitation.objects.get(slug=slug)
    except TeamInvitation.DoesNotExist:
        raise Http404()
    if not invitation.member == request.user:
        raise PermissionDenied()
    if request.user.team:
        messages.error(request, _("you already have a team"))
        return redirect('my_team')
    if invitation.team.member_set.count() == invitation.team.competition.max_members:
        messages.error(request, _("the team has reached max members"))
        return redirect('my_team')
    if invitation.team.final:
        messages.error(request, _("The team is final."))
    else:
        invitation.accept()
        messages.success(request, _('successfully joined team %s') % invitation.team.name)
        return redirect('my_team')
    return redirect('home')


@login_required
def teams(request):
    teams = Team.objects.exclude(show=False)
    if request.GET.get('final', '0') == '1':
        teams = teams.filter(final=True)

    show_friendly_button = False
    wait_time = 0
    if hasattr(request.user, 'team') and request.user.team:
        show_friendly_button = True
        if not request.user.team.final:
            show_friendly_button = False
        wait_time = GameRequest.check_last_time(request.user.team)
        if wait_time:
            show_friendly_button = False
        if not Submit.objects.filter(team=request.user.team).exists():
            show_friendly_button = False

    return render(request, 'custom/teams_list.html', {
        'teams': teams,
        # 'show_friendly_button': show_friendly_button,
        'show_friendly_button': False,
        'wait_time': wait_time,  # TODO: mjafar, you can show this in template(even a countdown!)
    })


@login_required
@team_required(register_period_only=True)
@require_POST
def change_team_name(request, id):
    team_name_form = TeamNameForm(request.POST, instance=Team.objects.get(id=id))
    if team_name_form.is_valid():
        if team_name_form.instance.head.pk != request.user.pk:
            raise PermissionDenied()
        if team_name_form.instance.final:
            messages.error(request, _("The team is final."))
            return redirect('my_team')
        team_name_form.save()

    return redirect('my_team')


@login_required
@team_required
def my_team(request):
    if request.method == 'POST':
        will_come_form = WillComeForm(request.POST, instance=request.team)
        if will_come_form.is_valid():
            will_come_form.save()
            return redirect('my_team')
    else:
        will_come_form = WillComeForm(instance=request.team)
    for message in Message.objects.filter(to_date__gte=timezone.now(), from_date__lte=timezone.now()):
        if get_language_from_request(request).startswith('en'):
            messages.info(request, message.english_text)
        else:
            messages.info(request, message.persian_text)
    team = request.team
    team_name_form = TeamNameForm(instance=team)
    invited_members = TeamInvitation.objects.filter(team=team, accepted=False).select_related('member').all()
    join_requests = JoinRequest.objects.filter(team=team, accepted__isnull=True).select_related('member').all()
    return render(request, 'custom/my_team.html', {
        'team': team,
        'team_name_form': team_name_form,
        'invited_members': invited_members,
        'join_requests': join_requests,
        'will_come_form': will_come_form,
    })


@login_required
@team_required
def my_games(request):
    if not request.team.final:
        messages.error(request, _('your team must be final'))
        return redirect('my_team')

    participations = GameTeamSubmit.objects.filter(submit__team=request.team).select_related('game')
    sent_requests = GameRequest.objects.filter(requester=request.team)
    received_requests = GameRequest.objects.filter(requestee=request.team)

    return render(request, 'custom/my_games.html', context={
        'team': request.user.team,
        'participations': participations,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })


@login_required
@team_required
@require_POST
def handle_game_request(request):
    if not request.team.final:
        return HttpResponse(json.dumps({
            'success': False,
            'message': str(_('your team must be final'))
        }), content_type='application/json')

    try:
        game_request = GameRequest.objects.get(id=request.POST.get('id'), requestee=request.team)
    except GameRequest.DoesNotExist:
        return HttpResponse(json.dumps({
            'success': False,
            'message': str(_('No such game request found'))
        }), content_type='application/json')

    if 'status' not in request.POST or request.POST.get('status') not in {'accept', 'reject'}:
        return HttpResponse(json.dumps({
            'success': False,
            'message': str(_('Bad request'))
        }), content_type='application/json')
    else:
        accept = request.POST['status'] == 'accept'

    wait = game_request.accept(accept)
    if wait:
        return HttpResponse(json.dumps({
            'success': False,
            'message': str(_('this team can not play for %d minutes') % wait)
        }), content_type='application/json')

    return HttpResponse(json.dumps({
        'success': True,
        'message': str(_('Done'))
    }), content_type='application/json')


@login_required
@team_required
@require_POST
def game_request(request):
    if not request.team.final:
        messages.error(request, _('your team must be final'))
        return HttpResponseRedirect(reverse('teams_list') + '?final=1')

    if 'team_id' not in request.POST:
        return HttpResponseBadRequest()

    try:
        team = Team.objects.get(id=request.POST.get('team_id'))
    except Team.DoesNotExist:
        raise Http404()

    wait = GameRequest.create(requester=request.team, requestee=team)
    if wait:
        messages.error(request, _('you must wait %d minutes before another request') % wait)
        return HttpResponseRedirect(reverse('teams_list') + '?final=1')

    messages.info(request, _('Challenged the team successfully'))
    return redirect('my_games')


@login_required
@team_required
def compile_log(request):
    if 'submission_id' not in request.GET:
        return HttpResponseBadRequest()

    submit_object = get_object_or_404(Submit, pk=request.GET.get('submission_id'))
    if submit_object.team != request.team:
        raise PermissionDenied()

    return HttpResponse(submit_object.compile_log_file)


@login_required
@team_required
@require_POST
def remove(request):
    if registration_period_ended(request):
        return HttpResponse(json.dumps({"success": False, "message": str(_("registration period has ended"))}),
                            content_type='application/json')
    type = request.POST.get('type')
    id = request.POST.get('id')
    if type == 'team':
        team = Team.objects.get(pk=id)
        is_head = request.team.head == request.user
        if not is_head or team != request.team or team.final:
            if team.final:
                messages.error(request, _("The team is final."))
            raise PermissionDenied()
        team.delete()
    elif type == 'member':
        member = Member.objects.get(pk=id)
        if not request.team.member_set.filter(id=id).exists():
            raise Http404()
        is_head = request.team.head == request.user
        if not is_head and member != request.user:
            raise PermissionDenied()
        if member.team.final:
            messages.error(request, _("The team is final."))
            raise PermissionDenied()
        member.team = None
        member.save()
    elif type == 'invitation':
        try:
            invitation = TeamInvitation.objects.get(pk=id)
        except TeamInvitation.DoesNotExist:
            raise Http404()
        is_head = request.team.head == request.user
        if not is_head or request.team.pk != invitation.team.pk:
            raise PermissionDenied()
        invitation.delete()
    else:
        return HttpResponse(json.dumps({"success": False}), content_type='application/json')

    return HttpResponse(json.dumps({"success": True}), content_type='application/json')


@login_required
@team_required
@require_POST
def finalize(request):
    if registration_period_ended(request):
        return HttpResponse(json.dumps({"success": False, "message": str(_("registration period has ended"))}),
                            content_type='application/json')
    id = request.POST.get('id')
    team = Team.objects.get(pk=id)
    is_head = request.team.head == request.user
    if not is_head or team != request.team:
        raise PermissionDenied()

    member_count = team.member_set.count()
    if member_count < team.competition.min_members or member_count > team.competition.max_members:
        return HttpResponse(json.dumps({
            'success': False,
            'message': _('your team does not have enough members').encode('utf-8')
        }), content_type='application/json')

    team.final = True
    team.save()

    return HttpResponse(json.dumps({
        "success": True,
        "message": _('team is now finalized').encode('utf-8')
    }), content_type='application/json')


@login_required
@team_required
@require_POST
def resend_invitation_mail(request):
    if registration_period_ended(request):
        return HttpResponse(json.dumps({"success": False, "message": str(_("registration period has ended"))}),
                            content_type='application/json')
    id = request.POST.get('id')
    try:
        invitation = TeamInvitation.objects.get(pk=id)
    except TeamInvitation.DoesNotExist:
        raise Http404()
    is_head = request.team.head == request.user
    if not is_head or request.team.pk != invitation.team.pk:
        raise PermissionDenied()

    send_mail_template(_('AIChallenge team invitation'), 'mail/invitation_mail', '', invitation.member.email,
                       context={
                           'team': invitation.team.name,
                           'abs_link': invitation.accept_link,
                           'current_host': request.get_host
                       })
    messages.info(request, _("please check spams too"))
    return HttpResponse(json.dumps({"success": True, "message": _("invitation resend successful")}),
                        content_type='application/json')


@login_required
@team_required
@require_POST
def accept_decline_request(request):
    if registration_period_ended(request):
        return HttpResponse(json.dumps({"success": False, "message": str(_("registration period has ended"))}),
                            content_type='application/json')
    try:
        req = JoinRequest.objects.get(pk=request.POST.get('id'))
    except JoinRequest.DoesNotExist:
        raise Http404()
    if req.team != request.team or req.team.head != request.user:
        raise PermissionDenied()
    type = request.POST.get('type', 'decline')
    success = True
    message = ""
    if type == 'decline':
        req.accepted = False
        req.save()
    elif type == 'accept':
        if req.member.team:
            success = False
            message = _("already part of another team")
        elif req.team.member_set.count() == req.team.competition.max_members:
            success = False
            message = _("the team has reached max members")
        else:
            req.accept()

    return HttpResponse(json.dumps({'success': success, 'message': str(message)}), content_type='application/json')


@login_required
def request_join(request, team_id):
    if registration_period_ended(request):
        messages.error(request, _("registration period has ended"))
        return redirect('teams_list')
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise Http404()
    if request.user.team:
        messages.error(request, _("you already have a team"))
    if team.member_set.count() == team.competition.max_members:
        messages.error(request, _("the team has reached max members"))
    elif team.final:
        messages.error(request, _("The team is final."))
    else:
        req, is_new = JoinRequest.objects.get_or_create(team=team, member=request.user)
        if is_new:
            send_mail_template(_('AIChallenge team join request'), 'mail/join_request_mail', '', team.head.email,
                               context={'member': request.user.get_full_name()})
            messages.success(request, _('join request has been sent'))
            messages.info(request, _("please check spams too"))
        else:
            if req.accepted is False:
                messages.error(request, _('your request to join this team has been declined'))
            else:
                messages.warning(request, _('you have requested to join this team before'))
    return redirect('teams_list')
