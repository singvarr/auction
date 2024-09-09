import stripe
from django.conf import settings
from auction.auction.models import Auction
from auction.user.models import User
from auction.auction.exceptions import InvalidAuctionStatusException
from auction.payment.redirect_urls import redirect_urls
from auction.payment.exceptions import (
    AuctionHasNoPaymentDetailsException,
    UserAlreadyEnrolledException,
)
from auction.payment.models import AuctionPaymentInfo


class PaymentService:
    def __init__(self) -> None:
        self._api_key = settings.STRIPE_API_KEY

    def enroll_auction(self, auction: Auction, user: User) -> str:
        if auction.status != Auction.Status.ACTIVE:
            raise InvalidAuctionStatusException()
        if not auction.auctionpaymentinfo:
            raise AuctionHasNoPaymentDetailsException()

        is_user_enrolled = Auction.objects.filter(user=user, pk=auction.pk).exists()

        if is_user_enrolled:
            raise UserAlreadyEnrolledException()

        session = stripe.checkout.Session.create(
            ui_mode="embedded",
            mode="payment",
            return_url=redirect_urls["SUCCESS_PAYMENT_URL"],
            cancel_url=redirect_urls["CANCEL_PAYMENT_URL"],
            line_items=[
                {
                    "price": auction.access_fee,
                    "quantity": 1,
                }
            ],
            metadata={"user_id": user.pk},
        )

        return session.url

    def save_auction_payment_details(self, auction: Auction):
        if not auction.requires_payment or not auction.access_fee:
            raise InvalidAuctionStatusException()

        product = stripe.Product.create(
            name=f"Auction for {auction.lot.name}",
            description=auction.lot.description,
            images=[auction.lot.image.url],
        )

        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(auction.access_fee * 100),
            currency="usd",
        )

        AuctionPaymentInfo.objects.update_or_create(
            auction=auction,
            defaults={
                "price_id": price["id"],
                "product_id": product["id"],
            },
            create_defaults={
                "price_id": price["id"],
                "product_id": product["id"],
                "auction": auction,
            },
        )
