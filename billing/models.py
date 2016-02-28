from django.db import models
from base.models import Member
from django.utils.crypto import get_random_string
from suds.client import Client
from django.core.urlresolvers import reverse


class Transaction(models.Model):
    STATE = (
        ('u', 'unknown'),
        ('v', 'valid'),
        ('c', 'cancelled')
    )
    BANK = {
        'mellat': 1, 'tejarat': 2
    }

    user = models.ForeignKey(Member, related_name='transactions')
    amount = models.PositiveSmallIntegerField()
    status = models.CharField(choices=STATE, max_length=1)
    our_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    bank = models.CharField(max_length=1, choices=[(str(v), k) for k,v in BANK.items()])
    reference_id = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @classmethod
    def begin_transaction(cls, user, code_melli, amount, bank='mellat'):
        """
        :param user:
        :param amount: in rials
        :param bank: 'mellat' or 'tejarat'
        :return: (url, transaction)
        """
        random_string = get_random_string(length=100)
        t = Transaction.objects.create(
            user=user,
            amount=amount,
            status='u',
            bank=bank,
            our_id=random_string
        )
        from django.conf import settings
        username = settings.BANK_USERNAME
        password = settings.BANK_PASSWORD
        group_id = settings.BANK_GROUP_ID

        phone = user.phone_number
        if len(phone) < 7:
            phone = '%s%s' % ('0'*(7-len(phone)), phone)
        elif len(phone) > 7:
            phone = phone[:7]

        mobile = user.phone_number
        if mobile[:2] != '09':
            mobile = '09{}'.format(mobile)

        params = {
            'groupid': group_id,
            'username': username,
            'password': password,
            'bankid': cls.BANK[bank],
            'id2': random_string,
            'callbackurl': reverse('bank_callback') + '?',
            'nc': code_melli,
            'name': user.first_name,
            'family': user.last_name,
            'tel': phone,
            'mobile': mobile,
            'email': user.email,
            'amount': amount,
            'memo': t.pk,
        }

        def call_webservice(params):
            cl = Client('http://payment.sharif.ir/research/ws.asmx')
            return cl.service.Request(params)

        rescode, order_id = call_webservice(params).split(',')
        t.order_id = order_id
        t.save()
        if rescode == '0':
            return 'http://payment.sharif.ir/research/submit.aspx?orderid={}'.format(order_id), t
        else:
            t.status = 'c'
            t.save()
            return '', t

    def update_status(self):
        from django.conf import settings
        username = settings.BANK_USERNAME
        password = settings.BANK_PASSWORD
        group_id = settings.BANK_GROUP_ID

        params = {
            'groupid': group_id,
            'username': username,
            'password': password,
            'bankid': self.BANK[self.bank],
            'orderid': self.order_id
        }
        def call_webservice(params):
            cl = Client('http://payment.sharif.ir/research/ws.asmx')
            return cl.service.Status(params)

        vercode, reference_id = call_webservice(params).split(':')
        self.reference_id = reference_id
        if vercode == '0':
            self.status = 'v'
        else:
            self.status = 'c'
        self.save()

        return reference_id
