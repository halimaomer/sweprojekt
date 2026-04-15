# ruff: noqa: S101, D103

"""Tests für GET mit Pfadparameter für die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("hotel_id", [30, 1, 20])
def test_get_by_id_admin(hotel_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{hotel_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == hotel_id


@mark.rest
@mark.get_request
@mark.parametrize("hotel_id", [0, 999999])
def test_get_by_id_not_found(hotel_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{hotel_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_hotel() -> None:
    # arrange
    hotel_id: Final = 20
    token: Final = login(username="alice")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{hotel_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    hotel_id_response: Final = response_body.get("id")
    assert hotel_id_response is not None
    assert hotel_id_response == hotel_id
