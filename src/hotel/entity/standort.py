"""Entity-Klasse für den Standort."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel.entity.base import Base


class Standort(Base):
    """Entity-Klasse für den Standort."""

    __tablename__ = "standort"

    strasse: Mapped[str]
    """Die Straße."""

    hausnummer: Mapped[str]
    """Die Hausnummer."""

    plz: Mapped[str]
    """Die Postleitzahl."""

    ort: Mapped[str]
    """Der Ort."""

    land: Mapped[str]
    """Das Land."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), unique=True)
    """ID des zugehörigen Hotels als Fremdschlüssel in der DB-Tabelle."""

    hotel: Mapped[Hotel] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
    back_populates="standort",
    )
    """Das zugehörige transiente Hotel-Objekt."""

    def __repr__(self) -> str:
        """Ausgabe eines Standorts als String ohne die Hoteldaten."""
        return (
            f"Standort(id={self.id}, "
            f"strasse={self.strasse}, hausnummer={self.hausnummer}, "
            f"plz={self.plz}, ort={self.ort}, land={self.land})"
        )
