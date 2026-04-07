"""Pydantic-Model zum Aktualisieren von Hoteldaten."""

from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, StringConstraints

from hotel.entity.hotel import Hotel

__all__ = ["HotelUpdateModel"]


class HotelUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren von Hoteldaten."""

    name: Annotated[str, StringConstraints(max_length=64)]
    """Der Name des Hotels."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Hotel am Markt"
            }
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary.

        :return: Dictionary mit den primitiven Hotel-Attributen
        :rtype: dict[str, Any]
        """
        hotel_dict = self.model_dump()
        hotel_dict["id"] = None
        hotel_dict["standort"] = None
        hotel_dict["zimmer"] = []
        hotel_dict["erzeugt"] = None
        hotel_dict["aktualisiert"] = None

        return hotel_dict

    def to_hotel(self) -> Hotel:
        """Konvertierung in ein Hotel-Objekt für SQLAlchemy.

        :return: Hotel-Objekt für SQLAlchemy
        :rtype: Hotel
        """
        logger.debug("self={}", self)
        hotel_dict = self.to_dict()

        hotel = Hotel(**hotel_dict)
        logger.debug("hotel={}", hotel)
        return hotel
