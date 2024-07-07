from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from auction.auction.models import Auction, AuctionBid
from auction.auction.services.manage_status_auction import ManageStatusAuctionService
from auction.auction.serializers import (
    AuctionBidSerializer,
    CreateUpdateAuctionSerializer,
    ListAuctionSerializer,
    RetrieveAuctionSerializer,
)
from auction.auction.services.crud_auction import AuctionCRUDService


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
        if self.request.method == "POST":
            return [IsAdminUser()]

        return MethodNotAllowed(method=self.request.method)

    def get_queryset(self):
        return (
            Auction.objects
            .select_related("lot")
            .prefetch_related("auctionbid_set")
            .annotate(bids=Count("auctionbid"))
            .all()
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListAuctionSerializer
        if self.request.method == "POST":
            return RetrieveAuctionSerializer

        return MethodNotAllowed(method=self.request.method)

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

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        if self.request.method == "PUT":
            return [IsAdminUser()]

        return MethodNotAllowed(method=self.request.method)

    def update(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        input_serializer = CreateUpdateAuctionSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = AuctionCRUDService(data=input_serializer.validated_data)
        auction = service.update(auction=auction)

        output_serializer = RetrieveAuctionSerializer(instance=auction)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class StartAuctionView(APIView):
    http_method_names = ["post"]
    permission_classes = [IsAdminUser]

    def post(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        service = ManageStatusAuctionService(auction=auction)
        started_auction = service.start()

        output_serializer = RetrieveAuctionSerializer(instance=started_auction)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)


class FinishAuctionView(APIView):
    http_method_names = ["post"]
    permission_classes = [IsAdminUser]

    def post(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        service = ManageStatusAuctionService(auction=auction)
        finished_auction = service.finish()

        output_serializer = RetrieveAuctionSerializer(instance=finished_auction)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class ListAuctionBidView(ListAPIView):
    serializer_class = AuctionBidSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("value", "created_at",)
    ordering = ("-created_at",)

    def get_queryset(self):
        auction_id = self.kwargs["pk"]
        get_object_or_404(Auction, pk=auction_id)

        return AuctionBid.objects.filter(auction_id=auction_id)
