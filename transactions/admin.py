from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type_transaction", "amount", "created_at", "updated_at",)
    list_filter = (
        ("created_at", DateFieldListFilter),
        ("updated_at", DateFieldListFilter),
    )
    search_fields = ("type_transaction", "created_at", "updated_at")
