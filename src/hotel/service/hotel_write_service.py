"""Geschäftslogik zum Schreiben von Hoteldaten."""

from typing import Final

from loguru import logger

from hotel.entity.hotel import Hotel
from hotel.repository.hotel_repository import HotelRepository, Session
from hotel.service.exceptions import NotFoundError, VersionOutdatedError
from hotel.service.hotel_dto import HotelDTO
from hotel.service.mailer import send_mail

__all__ = ["HotelWriteService"]


class HotelWriteService:
    """Service-Klasse mit Geschäftslogik für Hotels."""

    def __init__(self, repo: HotelRepository) -> None:
        """Konstruktor mit abhängigem HotelRepository."""
        self.repo: HotelRepository = repo

    def create(self, hotel: Hotel) -> HotelDTO:
        """Ein neues Hotel anlegen.

        :param hotel: Das neue Hotel
        :return: Das neu angelegte Hotel mit generierter ID
        """
        logger.debug(
            "hotel={}, standort={}, zimmer={}",
            hotel,
            hotel.standort,
            hotel.zimmer,
        )

        with Session() as session:
            hotel_db: Final = self.repo.create(hotel=hotel, session=session)
            hotel_dto: Final = HotelDTO(hotel_db)
            session.commit()

        send_mail(hotel_dto=hotel_dto)
        logger.debug("hotel_dto={}", hotel_dto)
        return hotel_dto

    def update(self, hotel: Hotel, hotel_id: int, version: int) -> HotelDTO:
        """Daten eines Hotels ändern.

        :param hotel: Die neuen Daten
        :param hotel_id: ID des zu aktualisierenden Hotels
        :param version: Version für optimistische Synchronisation
        :return: Das aktualisierte Hotel
        :rtype: HotelDTO
        :raises NotFoundError: Falls der zu aktualisierende Patient nicht existiert
        :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
        """
        logger.debug("hotel_id={}, version={}, {}", hotel_id, version, hotel)

        with Session() as session:
            if (
                hotel_db := self.repo.find_by_id(
                    hotel_id=hotel_id, session=session
                )
            ) is None:
                raise NotFoundError(hotel_id)
            if hotel_db.version > version:
                raise VersionOutdatedError(version)

            hotel_db.set(hotel)
            if (
                hotel_updated := self.repo.update(hotel=hotel_db, session=session)
            ) is None:
                raise NotFoundError(hotel_id)
            hotel_dto: Final = HotelDTO(hotel_updated)
            logger.debug("{}", hotel_dto)

            session.commit()
            hotel_dto.version += 1
            return hotel_dto

    def delete_by_id(self, hotel_id: int) -> None:
        """Ein Hotel anhand seiner ID löschen.

        :param hotel_id: ID des zu löschenden Hotels
        """
        logger.debug("hotel_id={}", hotel_id)
        with Session() as session:
            self.repo.delete_by_id(hotel_id=hotel_id, session=session)
            session.commit()
