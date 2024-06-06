from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from transactions.models import Transaction
from user.models import User


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "transaction_count", "transactions_list", "id", "is_staff")
    search_fields = ("username",)
    list_filter = ("is_staff",)

    inlines = [TransactionInline]

    def transaction_count(self, obj):
        return obj.transactions.count()

    transaction_count.short_description = "Transaction Count"

    def transactions_list(self, obj):
        transactions = obj.transactions.all()
        transaction_list = "<ul>"
        for transaction in transactions[:5]:
            transaction_list += f"<li>{transaction.type_transaction}: {transaction.amount}</li>"
        transaction_list += "</ul>"
        return format_html(transaction_list)
    transactions_list.short_description = "Transactions"


admin.site.register(User, UserAdmin)
