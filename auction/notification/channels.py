from enum import Enum


class Channels(str, Enum):
    GENERAL = "general"
    AUCTION = "presence-auction-{ID}"
