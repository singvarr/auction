from django.urls import path
from auction.notification.views import NotificationAuthView

app_name = "notifications"

urlpatterns = [path(route="auth/", view=NotificationAuthView.as_view(), name="auth")]
