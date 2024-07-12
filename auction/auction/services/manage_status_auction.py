from datetime import datetime
from auction.auction.models import Auction
from auction.auction.exceptions import InvalidAuctionStatusException
from auction.notification.service import NotificationService


class ManageStatusAuctionService:
    def __init__(self, auction: Auction) -> None:
        self._auction = auction
        self._notification_service = NotificationService()

    def start(self) -> Auction:
        if self._auction.status != Auction.Status.NOT_CONDUCTED:
            raise InvalidAuctionStatusException(detail=f"Cannot start an auction with status {self._auction.status}")

        self._auction.start_at = datetime.now()
        self._auction.status = Auction.Status.ACTIVE
        self._auction.save()

        self._notification_service.send_notification_about_started_auction(auction=self._auction)

        return self._auction

    def finish(self) -> Auction:
        if self._auction.status != Auction.Status.ACTIVE:
            raise InvalidAuctionStatusException(detail=f"Cannot finish an auction with status {self._auction.status}")

        self._auction.finished_at = datetime.now()
        self._auction.status = Auction.Status.FINISHED
        self._auction.save()

        self._notification_service.send_notification_about_finished_auction(auction=self._auction)

        return self._auction
