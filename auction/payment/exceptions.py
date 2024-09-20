from rest_framework import status
from rest_framework.exceptions import APIException


class CannotSyncAuctionWithoutEnabledPaymentException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "CANNOT_SYNC_AUCTION_DETAILS_WITHOUT_ENABLED_PAYMENT"
    default_detail = "Cannot sync auction details without enabled payment"


class UserAlreadyEnrolledException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "USER_ALREADY_ENROLLED"
    default_detail = "User already enrolled at auction and paid access fee"


class AuctionHasNoPaymentDetailsException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
