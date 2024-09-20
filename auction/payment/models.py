from django.db import models
from auction.auction.models import Auction


class AuctionPaymentInfo(models.Model):
    price_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE)
