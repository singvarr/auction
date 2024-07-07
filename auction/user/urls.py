from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from auction.user.views import RegisterUserView

app_name = "user"

urlpatterns = [
    path(route="register/", view=RegisterUserView.as_view(), name="register"),
    path("login/", view=TokenObtainPairView.as_view(), name="login"),
    path("refresh/", view=TokenRefreshView.as_view(), name="refresh"),
    path("revoke/", view=TokenBlacklistView.as_view(), name="revoke"),
]
