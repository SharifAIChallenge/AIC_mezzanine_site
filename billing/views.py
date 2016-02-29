from base.views import team_required
from billing.forms import UserCompletionForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from .models import Transaction
from django.shortcuts import redirect, render


@team_required
def payment(request):
    transaction = Transaction.objects.filter(status='v', user__in=request.team.member_set)
    if len(transaction) > 0:
        # Already paid
        return render(request, 'custom/bank_payment.html', {
            'paid': True
        })
    else:
        if request.method == 'POST':
            form = UserCompletionForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                url, t = Transaction.begin_transaction(form.instance, 1000000)
                if len(url) > 0:
                    return HttpResponseRedirect(url)
        else:
            form = UserCompletionForm(instance=request.user)
        return render(request, 'custom/bank_payment.html', {
            'paid': False,
            'form': form
        })


def bank_callback(request):
    our_id = request.GET.get('id2', None)
    if not our_id:
        raise PermissionDenied()

    try:
        transaction = Transaction.objects.get(our_id=our_id)
    except Transaction.DoesNotExist:
        raise PermissionDenied()

    transaction.update_status()
    success = True
    if transaction.status == 'v':
        transaction.user.team.set_paid(True)
    else:
        success = False

    # TODO: save success somewhere in session or messages or something

    return redirect('my_team')