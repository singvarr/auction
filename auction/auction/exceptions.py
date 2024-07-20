from rest_framework import status
from rest_framework.exceptions import APIException


error_messages = {
    "AUCTION_START_FAILURE": "Cannot start an auction with status {status}",
    "AUCTION_FINISH_FAILURE": "Cannot finish an auction with status {status}",
    "AUCTION_EDIT_FAILURE": "Cannot edit details of {status} auction",
}


class InvalidAuctionStatusException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "INVALID_AUCTION_STATUS"
    default_detail = "Action not allowed because auction status is invalid"


class InvalidBidValueException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "INVALID_BID_VALUE"
    default_detail = "Cannot set bid value"
