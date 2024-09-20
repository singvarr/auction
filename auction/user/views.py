from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from auction.user.serializers import RegisterUserSerializer, RetrieveUserSerializer
from auction.user.models import User


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer
    parser_classes = [MultiPartParser]


class RetrieveUserView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveUserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), email=self.kwargs["email"])
