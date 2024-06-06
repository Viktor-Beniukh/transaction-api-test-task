from django.conf import settings
from django.db import models


class Transaction(models.Model):
    type_transaction = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.type_transaction
