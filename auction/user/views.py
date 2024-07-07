from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from auction.user.serializers import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer
    parser_classes = [MultiPartParser]
