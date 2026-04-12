"""Entity-Klasse für Zimmer."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hotel.entity.base import Base


class Zimmer(Base):
    """Entity-Klasse für Zimmer."""

    __tablename__ = "zimmer"

    preis: Mapped[Decimal]
    """Der Preis des Zimmers."""

    zimmernummer: Mapped[str]
    """""Die Zimmernummer des Zimmers."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    """ID des zugehörigen Hotels als Fremdschlüssel in der DB-Tabelle."""

    hotel: Mapped[Hotel] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
    back_populates="zimmer",
    )
    """Das zugehörige transiente Hotel-Objekt."""

    def __repr__(self) -> str:
        """Ausgabe eines Zimmers als String ohne die Hoteldaten."""
        return (
            f"Zimmer(id={self.id}, preis={self.preis}, "
            + f"zimmernummer={self.zimmernummer}"
        )
