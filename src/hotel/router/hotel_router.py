"""HotelGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from hotel.repository import Pageable
from hotel.repository.slice import Slice
from hotel.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from hotel.router.dependencies import get_service
from hotel.router.page import Page
from hotel.security import Role, RolesRequired
from hotel.service import HotelDTO, HotelService

__all__ = ["hotel_router"]


hotel_router: Final = APIRouter(tags=["Lesen"])


@hotel_router.get(
    "/{hotel_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def get_by_id(
    hotel_id: int,
    request: Request,
    service: Annotated[HotelService, Depends(get_service)],
):
    """Suche mit der Hotel ID."""
    logger.debug("hotel_id={}", hotel_id)

    hotel: Final = service.find_by_id(hotel_id=hotel_id)
    logger.debug("hotel={}", hotel)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == hotel.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_hotel_to_dict(hotel),
        headers={ETAG: f'"{hotel.version}"'},
    )


@hotel_router.get("", dependencies=[Depends(RolesRequired(Role.ADMIN))])
def get(
    request: Request,
    service: Annotated[HotelService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter.

    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit Query-Parameter
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit einer Seite mit Hotel-Daten
    :rtype: Response
    :raises NotFoundError: Falls keine Hotels gefunden wurden
    """
    query_params: Final = request.query_params
    log_str: Final = "{}"
    logger.debug(log_str, query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    if "page" in query_params:
        del suchparameter["page"]
    if "size" in query_params:
        del suchparameter["size"]

    hotel_slice: Final = service.find(suchparameter=suchparameter, pageable=pageable)

    result: Final = _hotel_slice_to_page(hotel_slice, pageable)
    logger.debug(log_str, result)
    return JSONResponse(content=result)


@hotel_router.get("/name/{teil}", dependencies=[Depends(RolesRequired(Role.ADMIN))])
def get_name(
    teil: str,
    service: Annotated[HotelService, Depends(get_service)],
) -> JSONResponse:
    """Suche Namen zum gegebenen Teilstring.

    :param teil: Teilstring der gefundenen Namen
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 200 und gefundenen Namen im Body
    :rtype: Response
    :raises NotFoundError: Falls keine Name gefunden wurden
    """
    logger.debug("teil={}", teil)
    namen: Final = service.find_name(teil=teil)
    return JSONResponse(content=namen)


def _hotel_to_dict(hotel: HotelDTO) -> dict[str, Any]:
    hotel_dict: Final = asdict(obj=hotel)
    hotel_dict.pop("version")
    return hotel_dict


def _hotel_slice_to_page(
    hotel_slice: Slice[HotelDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    hotel_dict: Final = tuple(_hotel_to_dict(hotel) for hotel in hotel_slice.content)
    page: Final = Page.create(
        content=hotel_dict,
        pageable=pageable,
        total_elements=hotel_slice.total_elements,
    )
    return asdict(obj=page)
