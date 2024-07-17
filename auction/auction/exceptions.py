from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidAuctionStatusException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "INVALID_AUCTION_STATUS"
    default_detail = "Action not allowed because auction status is invalid"


class InvalidBidValueException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "INVALID_BID_VALUE"
    default_detail = "Cannot set bid value"
