# ruff: noqa: D103

"""Allgemeine Daten für die Tests."""

from http import HTTPStatus
from pathlib import Path
from ssl import create_default_context
from typing import Any, Final

from httpx import get, post

__all__ = [
    "base_url",
    "ctx",
    "db_populate",
    "db_populate_path",
    "graphql_path",
    "graphql_url",
    "health_url",
    "keycloak_populate",
    "keycloak_populate_path",
    "login",
    "login_graphql",
    "password_admin",
    "rest_path",
    "rest_url",
    "timeout",
    "token_path",
    "username_admin",
]

schema: Final = "https"
port: Final = 8000
# Fallback IPv6 -> IPv4 insbesondere bei Windows vermeiden; deshalb kein "localhost"
host: Final = "127.0.0.1"
base_url: Final = f"{schema}://{host}:{port}"

rest_path: Final = "/rest"
rest_url: Final = f"{base_url}{rest_path}"

health_url: Final = f"{base_url}/health"

graphql_path: Final = "/graphql"
graphql_url: Final = f"{base_url}{graphql_path}"

token_path: Final = "/auth/token"  # noqa: S105
db_populate_path: Final = "/dev/db_populate"
keycloak_populate_path: Final = "/dev/keycloak_populate"

username_admin: Final = "admin"
password_admin: Final = "p"  # noqa: S105  # NOSONAR

timeout: Final = 2
certificate: Final = str(Path("tests") / "integration" / "certificate.crt")
ctx = create_default_context(cafile=certificate)


def check_readiness() -> None:
    response: Final = get(f"{health_url}/readiness", verify=ctx)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"readiness mit Statuscode {response.status_code}")

    response_body: Final = response.json()
    if not isinstance(response_body, dict):
        raise RuntimeError("readiness ohne Dictionary im Response-Body")

    status: Final[Any | None] = response_body.get("db")
    if status != "up":
        raise RuntimeError(f"readiness mit Meldungstext {status}")


def login(
    username: str = username_admin,
    password: str = password_admin,  # NOSONAR
) -> str:
    login_data: Final = {"username": username, "password": password}
    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")

    response_body: Final = response.json()
    token: Final = response_body.get("token")
    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login() ohne gueltigen Token: {response_body}")

    return token


def login_graphql(
    username: str = username_admin,
    password: str = password_admin,  # NOSONAR
) -> str:
    return login(username=username, password=password)


def db_populate() -> None:
    response: Final = post(
        f"{base_url}{db_populate_path}",
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != HTTPStatus.NO_CONTENT:
        raise RuntimeError(f"db_populate() mit Statuscode {response.status_code}")


def keycloak_populate() -> None:
    response: Final = post(
        f"{base_url}{keycloak_populate_path}",
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != HTTPStatus.NO_CONTENT:
        raise RuntimeError(f"keycloak_populate() mit Statuscode {response.status_code}")
