from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from auction.user.models import User


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "is_active",
            "is_admin",
        )
        write_only_fields = ("password",)

    def to_internal_value(self, data):
        if data.get("password"):
            data["password"] = make_password(data["password"])

        return super().to_internal_value(data)
