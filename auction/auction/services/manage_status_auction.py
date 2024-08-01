from datetime import datetime
from django.db import transaction
from auction.auction.models import Auction
from auction.auction.exceptions import error_messages, InvalidAuctionStatusException
from auction.notification.service import NotificationService
from auction.auction.services.auction_bid import AuctionBidService


class ManageStatusAuctionService:
    def __init__(self, auction: Auction) -> None:
        self._auction = auction
        self._notification_service = NotificationService()
        self._auction_bid_service = AuctionBidService()

    def start(self) -> Auction:
        if self._auction.status != Auction.Status.NOT_CONDUCTED:
            raise InvalidAuctionStatusException(
                detail=error_messages["AUCTION_START_FAILURE"].format(
                    status=self._auction.status
                ),
            )

        self._auction.start_at = datetime.now()
        self._auction.status = Auction.Status.ACTIVE
        self._auction.save()

        self._notification_service.send_notification_about_started_auction(
            auction=self._auction
        )

        return self._auction

    def finish(self) -> Auction:
        if self._auction.status != Auction.Status.ACTIVE:
            raise InvalidAuctionStatusException(
                detail=error_messages["AUCTION_FINISH_FAILURE"].format(
                    status=self._auction.status
                ),
            )

        latest_bid = self._auction_bid_service.find_latest_bid(auction=self._auction)

        with transaction.atomic():
            self._auction.finished_at = datetime.now()
            self._auction.status = Auction.Status.FINISHED

            if latest_bid:
                self._auction.winner = latest_bid.made_by

                self._auction.lot.sold_price = latest_bid.value
                self._auction.lot.save()

            self._auction.save()

            self._notification_service.send_notification_about_finished_auction(
                auction=self._auction
            )

            return self._auction
