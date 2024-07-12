from enum import Enum


class EventTypes(str, Enum):
    CREATED_AUCTION = "auction:created"
    FINISHED_AUCTION = "auction:finished"
    STARTED_AUCTION = "auction:started"
