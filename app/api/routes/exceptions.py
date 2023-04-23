import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from app.api.routes.responses.exceptions import ErrorResult
from app.core.utils.exceptions import (MultipleEmailFound,
                                       NoEmailFound,
                                       MultipleUsernameFound,
                                       NoUsernameFound,
                                       EmailExist,
                                       UsernameExist)

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, exception_handler)


async def exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})

    match err:
        case NoUsernameFound() | NoEmailFound() as err:
            return ORJSONResponse(ErrorResult(message=err.message, data=err), status_code=status.HTTP_404_NOT_FOUND)
        case MultipleUsernameFound() | MultipleEmailFound() | EmailExist() | UsernameExist() as err:
            return ORJSONResponse(ErrorResult(message=err.message, data=err), status_code=status.HTTP_409_CONFLICT)
        case _:
            logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
            return ORJSONResponse(
                ErrorResult(message="Unknown server error has occurred", data=err),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
