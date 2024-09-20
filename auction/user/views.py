from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from auction.user.serializers import RegisterUserSerializer, RetrieveUserSerializer
from auction.user.models import User


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer
    parser_classes = [MultiPartParser]


class RetrieveUserView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveUserSerializer
