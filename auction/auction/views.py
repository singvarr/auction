from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Count
from django.http.response import HttpResponseRedirectBase
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from auction.auction.models import Auction, AuctionBid
from auction.auction.services.manage_status_auction import ManageStatusAuctionService
from auction.auction.serializers import (
    AuctionBidSerializer,
    CreateAuctionBidSerializer,
    CreateUpdateAuctionSerializer,
    ListAuctionSerializer,
    RetrieveAuctionSerializer,
)
from auction.auction.services.auction_crud import AuctionCRUDService
from auction.auction.services.auction_bid import AuctionBidService
from auction.auction.exceptions import (
    error_messages,
    InvalidAuctionStatusException,
    InvalidBidValueException,
)
from auction.common.base_error_serializer import BaseErrorSerializer
from auction.payment.service import PaymentService


class ListCreateAuctionView(ListCreateAPIView):
    parser_classes = [MultiPartParser]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ("status", "finished_at", "start_at", "bids")
    ordering = ("-start_at",)
    search_fields = ("lot__name",)
    filterset_fields = ("status", "start_at", "finished_at")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsAdminUser()]

    def get_queryset(self):
        return (
            Auction.objects.select_related("lot")
            .prefetch_related("auctionbid_set")
            .annotate(bids=Count("auctionbid"))
            .all()
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListAuctionSerializer

        return RetrieveAuctionSerializer

    @extend_schema(
        request=CreateUpdateAuctionSerializer,
        responses={status.HTTP_201_CREATED: RetrieveAuctionSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, **_):
        input_serializer = CreateUpdateAuctionSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = AuctionCRUDService(data=input_serializer.validated_data)
        auction = service.create()

        output_serializer = RetrieveAuctionSerializer(instance=auction)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class RetrieveUpdateAuctionView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser]
    queryset = Auction.objects.select_related("lot").all()
    serializer_class = RetrieveAuctionSerializer
    http_method_names = ["get", "put"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsAdminUser()]

    @extend_schema(
        request=CreateUpdateAuctionSerializer,
        responses={
            status.HTTP_200_OK: RetrieveAuctionSerializer,
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=BaseErrorSerializer,
                description=error_messages["AUCTION_EDIT_FAILURE"],
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        input_serializer = CreateUpdateAuctionSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = AuctionCRUDService(data=input_serializer.validated_data)
        auction = service.update(auction=auction)

        output_serializer = RetrieveAuctionSerializer(instance=auction)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)


class StartAuctionView(APIView):
    http_method_names = ["post"]
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: RetrieveAuctionSerializer,
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=BaseErrorSerializer,
                description=error_messages["AUCTION_START_FAILURE"],
            ),
        },
    )
    def post(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        service = ManageStatusAuctionService(auction=auction)
        started_auction = service.start()

        output_serializer = RetrieveAuctionSerializer(instance=started_auction)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)


class FinishAuctionView(APIView):
    http_method_names = ["post"]
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: RetrieveAuctionSerializer,
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=BaseErrorSerializer,
                description=error_messages["AUCTION_FINISH_FAILURE"],
            ),
        },
    )
    def post(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        service = ManageStatusAuctionService(auction=auction)
        finished_auction = service.finish()

        output_serializer = RetrieveAuctionSerializer(instance=finished_auction)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class CreateListAuctionBidView(ListCreateAPIView):
    serializer_class = AuctionBidSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = (
        "value",
        "created_at",
    )
    ordering = ("-created_at",)

    def get_queryset(self):
        auction_id = self.kwargs["pk"]
        get_object_or_404(Auction, pk=auction_id)

        return AuctionBid.objects.select_related("made_by").filter(
            auction_id=auction_id
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: AuctionBidSerializer(many=True),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=BaseErrorSerializer,
                description="Auction is not found",
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=CreateAuctionBidSerializer,
        responses={
            status.HTTP_201_CREATED: AuctionBidSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=BaseErrorSerializer,
                description="Auction is not found",
            ),
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=BaseErrorSerializer,
                description=InvalidAuctionStatusException.default_detail,
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
                response=BaseErrorSerializer,
                description=InvalidBidValueException.default_detail,
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, pk, **_):
        input_serializer = CreateAuctionBidSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        auction = get_object_or_404(Auction, pk=pk)

        service = AuctionBidService()
        bid = service.create(
            data=input_serializer.validated_data,
            user=request.user,
            auction=auction,
        )

        output_serializer = self.serializer_class(instance=bid)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class EnrollAuctionView(APIView):
    http_method_names = ["post"]

    def post(self, request, **_):
        auction_id = request.kwargs.get("pk")

        auction = get_object_or_404(Auction, auction_id)

        payment_service = PaymentService()
        session_url = payment_service.enroll_auction(auction=auction, user=request.user)

        return HttpResponseRedirectBase(
            status=status.HTTP_303_SEE_OTHER,
            redirect_to=session_url,
        )
