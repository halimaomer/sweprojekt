# ruff: noqa: S101, D103

"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark

token: str | None


@mark.rest
@mark.post_request
def test_post() -> None:
    neues_hotel: Final = {
        "name": "Hotel REST",
        "standort": {
            "strasse": "Reststrasse",
            "hausnummer": "1",
            "plz": "99999",
            "ort": "Restort",
            "land": "Deutschland",
        },
        "zimmer": [
            {
                "preis": "99.99",
                "zimmernummer": "101",
            }
        ],
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_hotel,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neues_hotel_invalid: Final = {
        "name": "X" * 100,
        "standort": {
            "strasse": "Reststrasse",
            "hausnummer": "1",
            "plz": "1234",
            "ort": "Restort",
            "land": "Deutschland",
        },
        "zimmer": [
            {
                "preis": "99.99",
                "zimmernummer": "101",
            }
        ],
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_hotel_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "name" in body or "string_too_long" in body


@mark.rest
@mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"name" "Hotel REST"}'
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=json_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "should be a valid dictionary" in response.text
