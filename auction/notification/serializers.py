from rest_framework.serializers import Serializer, CharField, ModelSerializer
from auction.user.models import User


class NotificationAuthInputSerializer(Serializer):
    socket_id = CharField()
    channel_name = CharField()


class NotificationAuthOutputSerializer(Serializer):
    class UserInfoSerializer(ModelSerializer):
        class Meta:
            fields = "first_name", "last_name", "avatar"
            model = User

    user_id = CharField()
    user_info = UserInfoSerializer()
