"""Repository fuer persistente Hoteldaten."""

from collections.abc import Mapping
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from hotel.entity.hotel import Hotel
from hotel.repository.pageable import Pageable
from hotel.repository.slice import Slice


class HotelRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Hotel."""

    def find_by_id(self, hotel_id: int | None, session: Session) -> Hotel | None:
        """Suche mit der Hotel-ID.

        :param hotel_id: ID des gesuchten Hotels
        :param session: Session für SQLAlchemy
        :return: Das gefundene Hotel oder None
        :rtype: Hotel | None
        """
        logger.debug("hotel_id={}", hotel_id)  # NOSONAR

        if hotel_id is None:
            return None

        statement: Final = (
            select(Hotel)
            .options(joinedload(Hotel.standort))
            .where(Hotel.id == hotel_id)
        )
        hotel: Final = session.scalar(statement)

        logger.debug("{}", hotel)
        return hotel

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Hotel]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter als Dictionary
        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Tupel, d.h. readonly Liste, der gefundenen Hotels oder leeres Tupel
        :rtype: Slice[Hotel]
        """
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        for key, value in suchparameter.items():
            if key == "name":
                hotels = self._find_by_name(
                    teil=value, pageable=pageable, session=session
                )
                logger.debug(log_str, hotels)
                return hotels
        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Hotel]:
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Hotel)
                .options(joinedload(Hotel.standort))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (select(Hotel).options(joinedload(Hotel.standort)))
        )
        hotels: Final = (session.scalars(statement)).all()
        anzahl: Final = self._count_all_rows(session)
        hotel_slice: Final = Slice(content=tuple(hotels), total_elements=anzahl)
        logger.debug("hotel_slice={}", hotel_slice)
        return hotel_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Hotel)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_name(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Hotel]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Hotel)
                .options(joinedload(Hotel.standort))
                .filter(Hotel.name.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Hotel)
                .options(joinedload(Hotel.standort))
                .filter(Hotel.name.ilike(f"%{teil}%"))
            )
        )
        hotels: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_name(teil, session)
        hotel_slice: Final = Slice(content=tuple(hotels), total_elements=anzahl)
        logger.debug("{}", hotel_slice)
        return hotel_slice

    def _count_rows_name(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Hotel)
            .filter(Hotel.name.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def create(self, hotel: Hotel, session: Session) -> Hotel:
        """Ein neues Hotel speichern.

        :param hotel: Die Daten des neuen Hotels
        :param session: Session für SQLAlchemy
        :return: Das neu angelegte Hotel mit generierter ID
        :rtype: Hotel
        """
        logger.debug(
            "hotel={}, hotel.standort={}, hotel.zimmer={}",
            hotel,
            hotel.standort,
            hotel.zimmer,
        )

        session.add(instance=hotel)

        session.flush(objects=[hotel])
        logger.debug("hotel_id={}", hotel.id)
        return hotel

    def update(self, hotel: Hotel, session: Session) -> Hotel | None:
        """Ein Hotel aktualisieren.

        :param hotel: Die neuen Hoteldaten
        :param session: Session für SQLAlchemy
        :return: Das aktualisierte Hotel oder None, falls kein Hotel mit der ID
        existiert
        :rtype: Hotel | None
        """
        logger.debug("{}", hotel)

        if (
            hotel_db := self.find_by_id(hotel_id=hotel.id, session=session)
        ) is None:
            return None

        logger.debug("{}", hotel_db)
        return hotel_db

    def delete_by_id(self, hotel_id: int, session: Session) -> None:
        """Die Daten zu einem Hotel löschen.

        :param hotel_id: Die ID des zu löschenden Hotels
        :param session: Session für SQLAlchemy
        """
        logger.debug("hotel_id={}", hotel_id)

        if (hotel := self.find_by_id(hotel_id=hotel_id, session=session)) is None:
            return
        session.delete(hotel)
        logger.debug("ok")
