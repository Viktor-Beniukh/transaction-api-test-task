from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer, TransactionListSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("user")
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """Retrieve the transaction with filter"""
        type_transaction = self.request.query_params.get("type_transaction")

        queryset = super().get_queryset()

        if type_transaction:
            queryset = queryset.filter(type_transaction__icontains=type_transaction)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TransactionListSerializer

        return super().get_serializer_class()
