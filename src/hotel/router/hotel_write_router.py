"""HotelWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from hotel.problem_details import create_problem_details
from hotel.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from hotel.router.dependencies import get_write_service
from hotel.router.hotel_model import HotelModel
from hotel.router.hotel_update_model import HotelUpdateModel
from hotel.service import HotelWriteService

__all__ = ["hotel_write_router"]


hotel_write_router: Final = APIRouter(tags=["Schreiben"])


@hotel_write_router.post("")
def post(
    hotel_model: HotelModel,
    request: Request,
    service: Annotated[HotelWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um ein neues Hotel anzulegen.

    :param hotel_model: Hoteldaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    :raises UsernameExistsError: Falls der Benutzername bereits existiert
    """
    logger.debug("hotel_model={}", hotel_model)
    hotel_dto: Final = service.create(hotel=hotel_model.to_hotel())
    logger.debug("hotel_dto={}", hotel_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{hotel_dto.id}"},
    )


@hotel_write_router.put("/{hotel_id}")
def put(
    hotel_id: int,
    hotel_update_model: HotelUpdateModel,
    request: Request,
    service: Annotated[HotelWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um ein Hotel zu aktualisieren.

    :param hotel_id: ID des zu aktualisierenden Hotels als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit If-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises ValidationError: Falls es bei Marshmallow Validierungsfehler gibt
    :raises NotFoundError: Falls zur id kein Hotel existiert
    :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "hotel_id={}, if_match={}, hotel_update_model={}",
        hotel_id,
        if_match_value,
        hotel_update_model,
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    hotel: Final = hotel_update_model.to_hotel()
    hotel_modified: Final = service.update(
        hotel=hotel,
        hotel_id=hotel_id,
        version=version_int,
    )
    logger.debug("hotel_modified={}", hotel_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{hotel_modified.version}"'},
    )


@hotel_write_router.delete("/{hotel_id}")
def hotel_id(
    hotel_id: int,
    service: Annotated[HotelWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um ein Hotel anhand seiner ID zu löschen.

    :param hotel_id: ID des zu löschenden Hotels
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("hotel_id={}", hotel_id)
    service.delete_by_id(hotel_id=hotel_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
