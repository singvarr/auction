from rest_framework.serializers import CharField, Serializer


class BaseErrorSerializer(Serializer):
    detail = CharField()
