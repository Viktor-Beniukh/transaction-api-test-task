from django.utils.dateparse import parse_datetime
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
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        updated_after = self.request.query_params.get("updated_after")
        updated_before = self.request.query_params.get("updated_before")

        queryset = super().get_queryset()

        if type_transaction:
            queryset = queryset.filter(type_transaction__icontains=type_transaction)

        if created_after:
            try:
                created_after_date = parse_datetime(created_after)
                if created_after_date:
                    queryset = queryset.filter(created_at__gte=created_after_date)
            except ValueError:
                pass

        if created_before:
            try:
                created_before_date = parse_datetime(created_before)
                if created_before_date:
                    queryset = queryset.filter(created_at__lte=created_before_date)
            except ValueError:
                pass

        if updated_after:
            try:
                updated_after_date = parse_datetime(updated_after)
                if updated_after_date:
                    queryset = queryset.filter(updated_at__gte=updated_after_date)
            except ValueError:
                pass

        if updated_before:
            try:
                updated_before_date = parse_datetime(updated_before)
                if updated_before_date:
                    queryset = queryset.filter(updated_at__lte=updated_before_date)
            except ValueError:
                pass

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
                description="Filter by type of transaction "
                            "(ex. ?type_transaction=Direct Transfer)",
            ),
            OpenApiParameter(
                "created_after",
                type=OpenApiTypes.DATETIME,
                description="Filter transactions created after this datetime "
                            "(ex. ?created_after=2024-01-01T00:00:00Z)",
            ),
            OpenApiParameter(
                "created_before",
                type=OpenApiTypes.DATETIME,
                description="Filter transactions created before this datetime "
                            "(ex. ?created_before=2024-01-01T00:00:00Z)",
            ),
            OpenApiParameter(
                "updated_after",
                type=OpenApiTypes.DATETIME,
                description="Filter transactions updated after this datetime "
                            "(ex. ?updated_after=2024-01-01T00:00:00Z)",
            ),
            OpenApiParameter(
                "updated_before",
                type=OpenApiTypes.DATETIME,
                description="Filter transactions updated before this datetime "
                            "(ex. ?updated_before=2024-01-01T00:00:00Z)",
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
