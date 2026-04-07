"""Pydantic-Model für das Hotel."""
from typing import Final

from loguru import logger
from pydantic import ConfigDict

from hotel.entity.hotel import Hotel
from hotel.router.hotel_update_model import HotelUpdateModel
from hotel.router.standort_model import StandortModel
from hotel.router.zimmer_model import ZimmerModel

__all__ = ["HotelModel"]


class HotelModel(HotelUpdateModel):
    """Pydantic-Model für die Hoteldaten."""

    standort: StandortModel
    """Der zugehörige Standort."""

    zimmer: list[ZimmerModel]
    """Die Liste der Zimmer."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Hotel am See",
                "standort": {
                    "strasse": "Muster Str.",
                    "hausnummer": "1a",
                    "plz": "12345",
                    "ort": "Musterstadt",
                    "land": "Deutschland"
                },
                "zimmer": [
                    {
                        "preis": "100",
                        "zimmernummer": "1"
                    },
                ],
            },
        }
    )

    def to_hotel(self) -> Hotel:
        """Konvertierung in ein Hotel-Objekt für SQLAlchemy.

        :return: Hotel-Objekt für SQLAlchemy
        :rtype: Hotel
        """
        logger.debug("self={}", self)
        hotel_dict = self.to_dict()

        hotel: Final = Hotel(**hotel_dict)
        hotel.standort = self.standort.to_standort()
        hotel.zimmer = [
            zimmer_model.to_zimmer() for zimmer_model in self.zimmer
        ]
        logger.debug("hotel={}", hotel)
        return hotel
