from typing import Optional
from auction.auction.models import Auction, AuctionBid
from auction.auction.exceptions import (
    InvalidAuctionStatusException,
    InvalidBidValueException,
)
from auction.user.models import User
from auction.notification.service import NotificationService


class AuctionBidService:
    def __init__(self) -> None:
        self._notification_service = NotificationService()

    def find_latest_bid(self, auction: Auction) -> Optional[AuctionBid]:
        return (
            AuctionBid.objects.filter(auction_id=auction.pk)
            .order_by("-created_at")
            .first()
        )

    def create(self, data, user: User, auction: Auction) -> AuctionBid:
        if auction.status != Auction.Status.ACTIVE:
            raise InvalidAuctionStatusException()

        value = data["value"]

        latest_bid = self.find_latest_bid(auction=auction)

        if (not latest_bid and value <= auction.lot.initial_price) or (
            latest_bid and value <= latest_bid.value
        ):
            raise InvalidBidValueException()

        new_bid = AuctionBid.objects.create(value=value, made_by=user, auction=auction)

        self._notification_service.send_notification_about_new_bid(
            bid=new_bid,
            socket_id=data["socket_id"],
        )

        return new_bid
