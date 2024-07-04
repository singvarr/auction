from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ValidationError
from auction.auction.models import Auction, Lot


class ListAuctionSerializer(ModelSerializer):
    class LotSerializer(ModelSerializer):
        class Meta:
            model = Lot
            fields = ("description",)

    lot = LotSerializer()

    class Meta:
        model = Auction
        fields = (
            "id",
            "status",
            "start_at",
            "finished_at",
            "lot",
        )


class CreateRetrieveUpdateAuctionSerializer(ModelSerializer):
    class LotSerializer(ModelSerializer):
        class Meta:
            model = Lot
            fields = (
                "id",
                "name",
                "initial_price",
                "description",
            )
            read_only_fields = ("id",)

    lot = LotSerializer()

    def validate_start_at(self, attr):
        if attr < timezone.now():
            raise ValidationError("Cannot select past date")

        return attr

    class Meta:
        model = Auction
        fields = (
            "id",
            "start_at",
            "lot",
        )
        read_only_fields = ("id",)
