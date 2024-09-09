from django.db import transaction
from auction.auction.models import Auction, Lot
from auction.auction.exceptions import error_messages
from auction.payment.service import PaymentService


class AuctionCRUDService:
    def __init__(self, data) -> None:
        self._data = data
        self._payment_service = PaymentService()

    def create(self) -> Auction:
        with transaction.atomic():
            lot = Lot.objects.create(
                name=self._data["name"],
                initial_price=self._data["initial_price"],
                description=self._data["description"],
                image=self._data["image"],
            )

            auction = Auction.objects.create(
                lot=lot,
                start_at=self._data["start_at"],
                access_fee=self._data["access_fee"],
                requires_payment=self._data["access_fee"] is None,
            )

            if auction.requires_payment:
                self._payment_service.save_auction_payment_details(auction=auction)

            return auction

    def update(self, auction: Auction) -> Auction:
        with transaction.atomic():
            if auction.status != Auction.Status.NOT_CONDUCTED:
                raise InvalidAuctionStatusException(
                    detail=error_messages["AUCTION_EDIT_FAILURE"].format(
                        status=auction.status
                    ),
                )

            initial_auction_access_fee = auction.access_fee

            auction.lot.name = self._data["name"]
            auction.lot.initial_price = self._data["initial_price"]
            auction.lot.description = self._data["description"]
            auction.lot.image = self._data["image"]
            auction.lot.save()

            auction.access_fee = self._data["access_fee"]
            auction.requires_payment = self._data["access_fee"] is None
            auction.start_at = self._data["start_at"]
            auction.save()

            if initial_auction_access_fee != auction.access_fee:
                self._payment_service.update_price(auction=auction)

            return auction
