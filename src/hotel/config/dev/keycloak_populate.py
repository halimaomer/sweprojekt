"""Neuladen von Keycloak im Modus DEV."""

from typing import Annotated, Final

from fastapi import Depends
from keycloak import KeycloakConnectionError
from loguru import logger

from hotel.config.dev_modus import dev_keycloak_populate
from hotel.security import Role, User, UserService
from hotel.security.dependencies import get_user_service

__all__ = [
    "KeycloakPopulateService",
    "get_keycloak_populate_service",
    "keycloak_populate",
]


utf8: Final = "utf-8"


class KeycloakPopulateService:
    """Service für das Neuladen von Keycloak im Modus DEV."""

    def __init__(self, user_service: UserService) -> None:
        """Konstruktor mit abhängigem hotelRepository."""
        self.user_service: UserService = user_service

    def populate(self) -> None:
        """User-Daten in Keycloak über die REST-Schnittstelle neu laden."""
        if not dev_keycloak_populate:
            return

        logger.warning(">>> Keycloak wird neu geladen <<<")
        try:
            self._remove_users()
            self._create_users()
            logger.warning(">>> Keycloak wurde neu geladen <<<")
        except KeycloakConnectionError:
            logger.error(">>> Keine Keycloak-Verbindung! Ist Keycloak gestartet? <<<")

    def _remove_users(self) -> None:
        self.user_service.remove_all_users()
        logger.debug("Alle User außer 'admin' geloescht")

    def _create_users(self) -> None:
        self.user_service.create_user(
            User(
                username="alice",
                email="alice@test.de",
                nachname="Alice",
                vorname="Alice",
                roles=[Role.PATIENT],
                password="p",  # noqa: S106
            )
        )


def get_keycloak_populate_service(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> KeycloakPopulateService:
    """Factory-Funktion für TokenService."""
    return KeycloakPopulateService(user_service)


def keycloak_populate():
    """Keycloak mit Testdaten neu laden, falls im dev-Modus."""
    if dev_keycloak_populate:
        service = get_keycloak_populate_service(get_user_service())
        service.populate()
