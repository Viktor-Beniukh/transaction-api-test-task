from django.urls import path, include
from rest_framework import routers

from user.views import CreateAdminView, LoginAdminView, LogoutAdminView, UserViewSet

router = routers.DefaultRouter()
router.register("clients", UserViewSet)

app_name = "user"


urlpatterns = [
    path("register-admin/", CreateAdminView.as_view(), name="create-admin"),
    path("login-admin/", LoginAdminView.as_view(), name="token"),
    path("logout-admin/", LogoutAdminView.as_view(), name="logout-admin"),
    path("", include(router.urls)),
]
