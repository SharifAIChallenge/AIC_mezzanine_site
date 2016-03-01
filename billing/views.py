from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect, render

from billing.forms import UserCompletionForm
from base.views import team_required
from .models import Transaction


@login_required
@team_required
def payment(request):
    if request.method == 'POST':
        form = UserCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            url, t = Transaction.begin_transaction(user=form.instance,
                                                   amount=request.team.payment_value,
                                                   callback_url=request.build_absolute_uri(reverse('complete_payment')) + '?')
            if url:
                return HttpResponseRedirect(url)
            else:
                return render(request, 'custom/bank_payment_error.html', context={
                    'error': t.error,
                })
    else:
        error = None
        if not request.team.should_pay:
            error = _("There is nothing to pay for.")
        if request.team.transactions.filter(status='v').exists():
            error = _("You have already paid.")
        if request.team.transactions.filter(status='u').exists():
            error = _("You have unverified payment(s).")
        if error:
            return render(request, 'custom/bank_payment_error.html', context={
                'error': error,
            })
        form = UserCompletionForm(instance=request.user)
        return render(request, 'custom/bank_payment.html', context={
            'form': form
        })


@login_required
@team_required
def complete_payment(request):
    our_id = request.GET.get('id2', None)
    if not our_id:
        raise PermissionDenied()

    transaction = get_object_or_404(Transaction, id=our_id)
    transaction.update_status()

    if transaction.status == 'v':
        return render(request, 'custom/bank_payment_success.html')
    elif transaction.status == 'c':
        return render(request, 'custom/bank_payment_error.html', context={
            'error': transaction.error,
        })
    else:
        return redirect('payments_list')


@login_required
@team_required
def payments_list(request):
    unknown_payments = Transaction.objects.filter(status='u')
    for transaction in unknown_payments:
        transaction.update_status()
    payments = request.team.transactions.all()
    return render(request, 'custom/bank_payments_list.html', context={
        'payments': payments,
    })
