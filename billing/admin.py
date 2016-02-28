from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'amount', 'status', 'our_id', 'order_id', 'bank', 'reference_id', 'created', 'updated']
    list_display = ['user', 'amount', 'status', 'bank', 'reference_id', 'updated']
