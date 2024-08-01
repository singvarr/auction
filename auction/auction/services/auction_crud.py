from django.db import transaction
from auction.auction.models import Auction, Lot
from auction.auction.exceptions import error_messages


class AuctionCRUDService:
    def __init__(self, data) -> None:
        self._data = data

    def create(self) -> Auction:
        with transaction.atomic():
            lot = Lot.objects.create(
                name=self._data["name"],
                initial_price=self._data["initial_price"],
                description=self._data["description"],
                image=self._data["image"],
            )

            auction = Auction.objects.create(lot=lot, start_at=self._data["start_at"])

            return auction

    def update(self, auction: Auction) -> Auction:
        with transaction.atomic():
            if auction.status != Auction.Status.NOT_CONDUCTED:
                raise InvalidAuctionStatusException(
                    detail=error_messages["AUCTION_EDIT_FAILURE"].format(
                        status=auction.status
                    ),
                )

            auction.lot.name = self._data["name"]
            auction.lot.initial_price = self._data["initial_price"]
            auction.lot.description = self._data["description"]
            auction.lot.image = self._data["image"]
            auction.lot.save()

            auction.start_at = self._data["start_at"]
            auction.save()

            return auction
