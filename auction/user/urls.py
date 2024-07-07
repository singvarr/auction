from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from auction.user.views import RegisterUserView

app_name = "user"

urlpatterns = [
    path(route="register/", view=RegisterUserView.as_view(), name="register"),
    path(route="login/", view=TokenObtainPairView.as_view(), name="login"),
    path(route="refresh/", view=TokenRefreshView.as_view(), name="refresh"),
    path(route="revoke/", view=TokenBlacklistView.as_view(), name="revoke"),
]
