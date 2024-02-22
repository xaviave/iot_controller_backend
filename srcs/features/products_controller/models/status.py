from enum import IntEnum


class Status(IntEnum):
    ON = 1
    OFF = 2
    ERROR = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
