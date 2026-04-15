# ruff: noqa: S101, D103, ARG005

"""Unit-Tests für find() von HotelService."""

from datetime import datetime
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from hotel.entity import Hotel, Standort
from hotel.repository import Pageable
from hotel.service import NotFoundError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "hotel.service.hotel_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_find
def test_find_by_name(hotel_service, session_mock) -> None:
    name = "Mockhotel"
    hotel_id = 1
    standort_mock = Standort(
        id=11,
        strasse="Hauptstrasse",
        hausnummer="1",
        plz="76133",
        ort="Karlsruhe",
        land="Deutschland",
        hotel_id=hotel_id,
        hotel=None,
    )
    hotel_mock = Hotel(
        id=hotel_id,
        name=name,
        standort=standort_mock,
        zimmer=[],
        version=0,
        erzeugt=datetime(2025, 1, 31, 0, 0, 0),
        aktualisiert=datetime(2025, 1, 31, 0, 0, 0),
    )
    standort_mock.hotel = hotel_mock
    suchparameter = {"name": name}
    pageable = Pageable(size=5, number=0)

    session_mock.scalars.return_value.all.return_value = [hotel_mock]

    hotels_slice = hotel_service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    assert len(hotels_slice.content) == 1
    assert hotels_slice.content[0].name == name


@mark.unit
@mark.unit_find
def test_find_by_name_not_found(hotel_service, session_mock) -> None:
    name = "Notfound"
    suchparameter = {"name": name}
    pageable = Pageable(size=5, number=0)

    session_mock.scalars.return_value.all.return_value = []

    with raises(NotFoundError) as err:
        hotel_service.find(suchparameter=suchparameter, pageable=pageable)

    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"
    assert err.value.suchparameter is not None
    assert err.value.suchparameter.get("name") == name
