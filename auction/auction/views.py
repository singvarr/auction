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
from django.db.models import Count
from auction.auction.models import Auction, AuctionBid
from auction.auction.services.manage_status_auction import ManageStatusAuctionService
from auction.auction.serializers import (
    AuctionBidSerializer,
    CreateRetrieveUpdateAuctionSerializer,
    ListAuctionSerializer,
)
from auction.auction.services.crud_auction import AuctionCRUDService


class ListCreateAuctionView(ListCreateAPIView):
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
            return CreateRetrieveUpdateAuctionSerializer
        return MethodNotAllowed(method=self.request.method)

    def create(self, request, **_):
        input_serializer = CreateRetrieveUpdateAuctionSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = AuctionCRUDService(data=input_serializer.data)
        auction = service.create()

        output_serializer = CreateRetrieveUpdateAuctionSerializer(instance=auction)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class RetrieveUpdateAuctionView(RetrieveUpdateAPIView):
    queryset = Auction.objects.select_related("lot").all()
    serializer_class = CreateRetrieveUpdateAuctionSerializer

    def update(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        input_serializer = CreateRetrieveUpdateAuctionSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = AuctionCRUDService(data=input_serializer.data)
        auction = service.update(auction=auction)

        output_serializer = CreateRetrieveUpdateAuctionSerializer(instance=auction)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class StartAuctionView(APIView):
    http_method_names = ["post"]

    def post(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        service = ManageStatusAuctionService(auction=auction)
        started_auction = service.start()

        output_serializer = ListAuctionSerializer(instance=started_auction)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)


class FinishAuctionView(APIView):
    http_method_names = ["post"]

    def post(self, request, pk, **_):
        auction = get_object_or_404(Auction, pk=pk)

        service = ManageStatusAuctionService(auction=auction)
        finished = service.finish()

        output_serializer = ListAuctionSerializer(instance=finished)

        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class ListAuctionBidView(ListAPIView):
    serializer_class = AuctionBidSerializer

    def get_queryset(self):
        auction_id = self.kwargs["pk"]
        get_object_or_404(Auction, pk=auction_id)

        return AuctionBid.objects.filter(auction_id=auction_id)
