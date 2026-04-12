"""Modul für die REST-Schnittstelle."""

from collections.abc import Sequence

from hotel.router.health_router import liveness, readiness
from hotel.router.health_router import router as health_router
from hotel.router.hotel_router import get, get_by_id, get_name, hotel_router
from hotel.router.hotel_write_router import (
    delete_by_id,
    hotel_write_router,
    post,
    put,
)
from hotel.router.shutdown_router import router as shutdown_router
from hotel.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "delete_by_id",
    "get",
    "get_by_id",
    "get_name",
    "health_router",
    "hotel_router",
    "hotel_write_router",
    "liveness",
    "post",
    "put",
    "readiness",
    "shutdown",
    "shutdown_router",
]
