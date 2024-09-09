from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from auction.notification.service import NotificationService


class Lot(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    initial_price = models.FloatField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="lots/", null=True, default=None)
    sold_price = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        default=True,
    )


class Auction(models.Model):
    class Status(models.TextChoices):
        NOT_CONDUCTED = "not_conducted", "Not conducted"
        ACTIVE = "active", "Active"
        FINISHED = "finished", "Finished"

    start_at = models.DateTimeField(null=True, default=None)
    finished_at = models.DateTimeField(null=True, default=None)
    status = models.CharField(
        choices=Status.choices,
        default=Status.NOT_CONDUCTED,
        max_length=255,
    )
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE)
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
    )
    requires_payment = models.BooleanField(default=False)
    access_fee = models.FloatField(
        validators=[MinValueValidator(0.01)],
        null=True,
        default=None,
    )

    def clean(self) -> None:
        if self.requires_payment and self.access_fee is None:
            raise ValidationError("Access fee is required when payment turned on")

        return super().clean()

    @receiver(post_save)
    def notify_about_new_auction(sender, instance, created, **_):
        if sender == Auction and created:
            service = NotificationService()
            service.send_notification_about_created_auction(auction=instance)


class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
