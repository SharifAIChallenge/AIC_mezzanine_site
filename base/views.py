# -*- coding: utf-8 -*-
import json
from functools import wraps
from urlparse import urlparse

from base.forms import SubmitForm, TeamForm, InvitationForm, TeamNameForm
from base.models import TeamInvitation, Team, Member, JoinRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from game.models import Competition
from mezzanine.utils.email import send_mail_template


def team_required(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'team') and request.user.team:
                request.team = request.user.team
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            messages.info(request,
                          _("you are not in a team, create one below or request your team leader to invite you"))
            resolved_login_url = reverse('register_team')
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
@team_required
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
                form.save(team=request.team)
                messages.success(request,
                                 _('successfully invited user %(name)s') % {'name': form.member.get_full_name()})
                return redirect('invite_member')
    else:
        form = InvitationForm()
    return render(request, 'accounts/invite_team.html', {'form': form, 'title': _('invite member to team')})


@login_required
@team_required
def submit(request):
    if request.team.member_set.count() < request.team.competition.min_members:
        messages.error(request, _("your team does not have enough members"))
        return redirect('invite_member')
    if request.method == 'POST':
        form = SubmitForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_submit = form.save(commit=False)
            new_submit.team = request.team
            new_submit.save()
            return redirect('submit_code')
    else:
        form = SubmitForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': _('submit new code')})


@login_required
def accept_invite(request, slug):
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
    else:
        invitation.accept()
        messages.success(request, _('successfully joined team %s') % invitation.team.name)
        return redirect('my_team')
    return redirect('home')


@login_required
def teams(request):
    teams = Team.objects.exclude(show=False).all()
    return render(request, 'custom/teams_list.html', {'teams': teams})


@login_required
@team_required
def change_team_name(request, id):
    if request.method != 'POST':
        raise PermissionDenied()
    team_name_form = TeamNameForm(request.POST, instance=Team.objects.get(id=id))
    if team_name_form.is_valid():
        if team_name_form.instance.head.pk != request.user.pk:
            raise PermissionDenied()
        team_name_form.save()

    return redirect('my_team')


@login_required
@team_required
def my_team(request):
    team = request.team
    team_name_form = TeamNameForm(instance=team)
    invited_members = TeamInvitation.objects.filter(team=team, accepted=False).select_related('member').all()
    join_requests = JoinRequest.objects.filter(team=team, accepted__isnull=True).select_related('member').all()
    return render(request, 'custom/my_team.html', {
        'team': team,
        'team_name_form': team_name_form,
        'invited_members': invited_members,
        'join_requests': join_requests,
    })


@login_required
@team_required
def remove(request):
    import json

    if request.method != 'POST':
        raise PermissionDenied()
    type = request.POST.get('type')
    id = request.POST.get('id')
    if type == 'team':
        team = Team.objects.get(pk=id)
        is_head = request.team.head == request.user
        if not is_head or team != request.team:
            raise PermissionDenied()
        team.delete()
    elif type == 'member':
        member = Member.objects.get(pk=id)
        if not request.team.member_set.filter(id=id).exists():
            raise Http404()
        is_head = request.team.head == request.user
        if not is_head and member != request.user:
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
def resend_invitation_mail(request):
    if request.method != 'POST':
        raise PermissionDenied()
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
                           'link': 'http://%s' % invitation.accept_link
                       })
    return HttpResponse(json.dumps({"success": True, "message": _("invitation resend successful")}),
                        content_type='application/json')


@login_required
@team_required
def accept_decline_request(request):
    if request.method != 'POST':
        raise PermissionDenied()
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
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise Http404()
    if request.user.team:
        messages.error(request, _("you already have a team"))
    if team.member_set.count() == team.competition.max_members:
        messages.error(request, _("the team has reached max members"))
    else:
        is_new = JoinRequest.objects.get_or_create(team=team, member=request.user)[1]
        if is_new:
            send_mail_template(_('AIChallenge team join request'), 'mail/join_request_mail', '', team.head.email,
                               context={'member': request.user.get_full_name()})
            messages.success(request, _('join request has been sent'))
        else:
            messages.warning(request, _('you have requested to join this team before'))
    return redirect('teams_list')
