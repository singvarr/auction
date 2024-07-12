from __future__ import annotations
from typing import TYPE_CHECKING
from auction.notification.channels import Channels
from auction.notification.event_types import EventTypes
from auction.notification.pusher import pusher_client

if TYPE_CHECKING:
    from auction.auction.models import Auction


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
        self._send_auction_event(event_type=EventTypes.FINISHED_AUCTION, auction=auction)
