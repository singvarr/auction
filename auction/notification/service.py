from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from auction.notification.channels import Channels
from auction.notification.event_types import EventTypes
from auction.notification.pusher import pusher_client


if TYPE_CHECKING:
    from auction.auction.models import Auction
    from auction.auction.models import AuctionBid


class NotificationService:
    def __init__(self) -> None:
        self._client = pusher_client

    def _send_auction_event(self, event_type: EventTypes, auction: Auction):
        self._client.trigger(Channels.GENERAL, event_type, {"auction_id": auction.pk})

    def send_notification_about_created_auction(self, auction: Auction):
        self._send_auction_event(event_type=EventTypes.CREATED_AUCTION, auction=auction)

    def send_notification_about_started_auction(self, auction: Auction):
        self._send_auction_event(event_type=EventTypes.STARTED_AUCTION, auction=auction)

    def send_notification_about_finished_auction(self, auction: Auction):
        self._send_auction_event(
            event_type=EventTypes.FINISHED_AUCTION, auction=auction
        )

    def send_notification_about_new_bid(self, bid: AuctionBid, socket_id: str):
        channel_name = Channels.AUCTION.format(id=bid.auction.pk)

        self._client.trigger(
            channels=channel_name,
            event_name=EventTypes.ADDED_BID,
            data={"latest_bid": bid.value},
            socket_id=socket_id,
        )

    def get_auction_id_from_channel_name(self, channel_name: str) -> Optional[int]:
        parts = channel_name.split("-")

        if (
            len(parts) == 3
            and parts[0] == "presence"
            and parts[1] == "auction"
            and parts[2].isnumeric()
        ):
            return int(parts[2])

        return None
