"""Entity-Klasse für Hoteldaten."""

from datetime import datetime
from typing import Any, Self

from sqlalchemy import Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel.entity.base import Base
from hotel.entity.standort import Standort
from hotel.entity.zimmer import Zimmer


class Hotel(Base):
    """Entity-Klasse für Hoteldaten."""

    __tablename__ = "hotel"

    name: Mapped[str]
    """Der Name des Hotels."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    standort: Mapped[Standort] = relationship(
        back_populates="hotel",
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Der in einer 1:1-Beziehung referenzierte Standort."""

    zimmer: Mapped[list[Zimmer]] = relationship(
        back_populates="hotel",
        cascade="save-update, delete",
    )
    """Die in einer 1:N-Beziehung referenzierten Zimmer."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )
    """Der Zeitstempel vom letzen UPDATE in der DB-Tabelle."""

    def set(self, hotel: Self) -> None:
        """Primitive Attributwerte aktualisieren, z.B. vor einem DB-Update."""
        """:param hotel: Hotel-Objekt mit den aktuellen Daten"""

        self.name: str = hotel.name

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleichheit mittels der ID."""
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Ausgabe eines Hotels als String."""
        return (
        f"Hotel(id={self.id}, name={self.name}, "
        f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert})"
        )
