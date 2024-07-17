from django.utils import timezone
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    FloatField,
    IntegerField,
    ImageField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from auction.auction.models import Auction, AuctionBid, Lot
from auction.user.models import User


class ListAuctionSerializer(ModelSerializer):
    class LotSerializer(ModelSerializer):
        class Meta:
            model = Lot
            fields = ("id", "name", "image")

    lot = LotSerializer()
    bids = IntegerField()

    class Meta:
        model = Auction
        fields = (
            "id",
            "status",
            "start_at",
            "finished_at",
            "lot",
            "bids",
        )


class CreateUpdateAuctionSerializer(Serializer):
    name = CharField(max_length=50)
    initial_price = FloatField(min_value=0)
    description = CharField()
    image = ImageField(allow_empty_file=True, allow_null=True, default=None)
    start_at = DateTimeField(allow_null=True, default=None)

    def validate_start_at(self, attr):
        if attr and attr < timezone.now():
            raise ValidationError("Cannot select past date")

        return attr


class RetrieveAuctionSerializer(ModelSerializer):
    class LotSerializer(ModelSerializer):
        class Meta:
            model = Lot
            fields = ("id", "name", "initial_price", "description", "image")

    lot = LotSerializer()

    class Meta:
        model = Auction
        fields = ("id", "start_at", "lot")
        read_only_fields = ("id",)


class AuctionBidSerializer(ModelSerializer):
    class UserSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = "id", "first_name", "last_name", "avatar"

    made_by = UserSerializer()

    class Meta:
        model = AuctionBid
        fields = "__all__"


class CreateAuctionBidSerializer(ModelSerializer):
    socket_id = CharField()

    class Meta:
        model = AuctionBid
        fields = "value", "socket_id"
