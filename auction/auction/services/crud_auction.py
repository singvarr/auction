from django.db import transaction
from auction.auction.models import Auction, Lot


class AuctionCRUDService:
    def __init__(self, data) -> None:
        self._data = data

    def create(self) -> Auction:
        with transaction.atomic():
            lot = Lot.objects.create(
                name=self._data["lot"]["name"],
                initial_price=self._data["lot"]["initial_price"],
                description=self._data["lot"]["description"],
            )

            auction = Auction.objects.create(lot=lot, start_at=self._data["start_at"])

            return auction

    def update(self, auction: Auction) -> Auction:
        with transaction.atomic():
            if auction.status != Auction.Status.NOT_CONDUCTED:
                raise InvalidAuctionStatusException(detail=f'Cannot edit details of {auction.status} auction')

            auction.lot.name = self._data["lot"]["name"]
            auction.lot.initial_price = self._data["lot"]["initial_price"]
            auction.lot.description = self._data["lot"]["description"]
            auction.lot.save()

            auction.start_at = self._data["start_at"]
            auction.save()

            return auction
