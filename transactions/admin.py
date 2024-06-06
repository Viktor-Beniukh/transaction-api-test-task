from django.contrib import admin

from transactions.models import Transaction


@admin.register(Transaction)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "type_transaction", "amount", "created_at", "updated_at",)
    list_filter = ("created_at",)
    search_fields = ("type_transaction", "created_at",)
