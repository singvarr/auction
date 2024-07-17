from rest_framework.serializers import Serializer, CharField


class NotificationAuthInputSerializer(Serializer):
    socket_id = CharField()
    channel_name = CharField()
