from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ("type_transaction", "amount", "user")


class TransactionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ("id", "type_transaction", "amount", "created_at", "updated_at", "user")
