from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidAuctionStatusException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "INVALID_AUCTION_STATUS"
    default_detail = "Action not allowed because auction status is invalid"
