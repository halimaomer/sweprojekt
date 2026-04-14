# ruff: noqa: S101, D103

"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

NAME_UPDATE: Final = "Hotel PUT"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    hotel_id: Final = 20
    if_match: Final = '"0"'
    geaendertes_hotel: Final = {
        "name": NAME_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    hotel_id: Final = 20
    geaendertes_hotel_invalid: Final = {
        "name": "X" * 100,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "If-Match": '"0"',
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "name" in response.text or "string_too_long" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    hotel_id: Final = 999999
    if_match: Final = '"0"'
    geaendertes_hotel: Final = {
        "name": NAME_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    hotel_id: Final = 20
    geaendertes_hotel: Final = {
        "name": NAME_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    hotel_id: Final = 20
    if_match: Final = '"-1"'
    geaendertes_hotel: Final = {
        "name": NAME_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    hotel_id: Final = 20
    if_match: Final = '"xy"'
    geaendertes_hotel: Final = {
        "name": NAME_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
    assert not response.text


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    hotel_id: Final = 20
    if_match: Final = "0"
    geaendertes_hotel: Final = {
        "name": NAME_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{hotel_id}",
        json=geaendertes_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
