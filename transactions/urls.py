from django.urls import path, include
from rest_framework import routers

from transactions.views import TransactionViewSet

router = routers.DefaultRouter()
router.register("transactions", TransactionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "transactions"
