from enum import Enum


class PeriodEnum(Enum):
    ONE_DAY     = (1, 1)
    TWO_DAYS    = (2, 2)
    THREE_DAYS  = (3, 3)
    ONE_WEEK    = (4, 7)
    TWO_WEEKS   = (5, 14)

    def __new__(cls, value, days):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.days = days
        return obj
