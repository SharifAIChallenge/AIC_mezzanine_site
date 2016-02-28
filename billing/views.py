from django.core.exceptions import PermissionDenied
from .models import Transaction
from django.shortcuts import redirect


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