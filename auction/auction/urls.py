from django.urls import path
from auction.auction.views import (
    ListAuctionBidView,
    FinishAuctionView,
    ListCreateAuctionView,
    RetrieveUpdateAuctionView,
    StartAuctionView,
)


app_name = "auction"

urlpatterns = [
    path(route="", view=ListCreateAuctionView.as_view(), name="list-create"),
    path(
        route="<int:pk>",
        view=RetrieveUpdateAuctionView.as_view(),
        name="retrieve-update",
    ),
    path(route="<int:pk>/start/", view=StartAuctionView.as_view(), name="start"),
    path(route="<int:pk>/finish/", view=FinishAuctionView.as_view(), name="finish"),
    path(route="<int:pk>/bids/", view=ListAuctionBidView.as_view(), name="bids"),
]
