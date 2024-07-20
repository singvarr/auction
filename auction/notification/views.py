from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from auction.notification.pusher import pusher_client
from auction.notification.serializers import (
    NotificationAuthInputSerializer,
    NotificationAuthOutputSerializer,
)
from auction.auction.models import Auction
from auction.notification.service import NotificationService
from auction.user.service import UserService
from auction.common.base_error_serializer import BaseErrorSerializer


class NotificationAuthView(APIView):
    http_method_names = ["post"]
    permission_classes = (AllowAny,)

    @extend_schema(
        request=NotificationAuthInputSerializer,
        description="The endpoint for authentication connection in auction channel",
        responses={
            status.HTTP_200_OK: NotificationAuthOutputSerializer,
            status.HTTP_403_FORBIDDEN: BaseErrorSerializer,
        }
    )
    def post(self, request, **_):
        """
        Pusher auth endpoint should return 403 error on failure of user authorization because Pusher requires this
        status code. However, DRF sends 401 error if token is expired even for public endpoint.
        """
        if not request.user.is_authenticated:
            return PermissionDenied(detail="User is not authenticated")

        input_serializer = NotificationAuthInputSerializer(data=request.data)
        is_valid = input_serializer.is_valid(raise_exception=False)

        if not is_valid:
            raise PermissionDenied(input_serializer.errors)

        service = NotificationService()

        channel_name = input_serializer.validated_data["channel_name"]
        auction_id = service.get_auction_id_from_channel_name(channel_name=channel_name)

        if not auction_id:
            raise PermissionDenied("Auction id is not provided or invalid")

        auction = Auction.objects.filter(pk=auction_id).first()

        if not auction:
            raise PermissionDenied("Auction is not found")
        if auction.status != Auction.Status.ACTIVE:
            raise PermissionDenied("Auction is not started")

        user_service = UserService()
        user_info = user_service.get_details_for_notifications(user=request.user)

        result = pusher_client.authenticate(
            socket_id=request.data["socket_id"],
            channel=request.data["channel_name"],
            custom_data={
                "user_id": request.user.pk,
                "user_info": user_info,
            },
        )

        return Response(status=status.HTTP_200_OK, data=result)
