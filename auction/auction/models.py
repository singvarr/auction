from django.db import models
from django.core.validators import MinValueValidator


class Lot(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    initial_price = models.FloatField(validators=[MinValueValidator(0)])
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


class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
