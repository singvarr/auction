from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from auction.user.models import User


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "is_active",
            "is_admin",
            "last_login",
            "auctions",
        )
        write_only_fields = ("password",)

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        return super().update(instance, validated_data)
