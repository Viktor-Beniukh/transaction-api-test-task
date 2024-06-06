from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "type_transaction",
                type=OpenApiTypes.STR,
                description="Filter by type of transaction (ex. ?type_transaction=Direct Transfer)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of transactions"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve a specific transaction",
        responses={200: TransactionListSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific transaction"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Create a new transaction",
        request=TransactionSerializer,
        responses={201: TransactionSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Create a new transaction"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing transaction",
        request=TransactionSerializer,
        responses={200: TransactionSerializer},
    )
    def update(self, request, *args, **kwargs):
        """Update an existing transaction"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing transaction",
        request=TransactionSerializer,
        responses={200: TransactionSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an existing transaction"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Delete an existing transaction",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing transaction"""
        return super().destroy(request, *args, **kwargs)
