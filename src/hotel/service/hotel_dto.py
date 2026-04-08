"""DTO-Klasse für Hoteldaten."""

from dataclasses import dataclass

import strawberry

from hotel.entity import Hotel
from hotel.service.standort_dto import StandortDTO

__all__ = ["HotelDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class HotelDTO:
    """DTO-Klasse für aus gelesene oder gespeicherte Hoteldaten: ohne Decorators."""

    id: int
    version: int
    name: str
    standort: StandortDTO

    def __init__(self, hotel: Hotel) -> None:
        """Initialisierung von HotelDTO durch ein Entity-Objekt von Hotel.

        :param hotel: Hotel-Objekt mit Decorators für SQLAlchemy
        """
        hotel_id = hotel.id
        self.id = hotel_id if hotel_id is not None else -1
        self.version = hotel.version
        self.name = hotel.name
        self.standort = StandortDTO(hotel.standort)
