import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.config.models.api import AuthConfig, ApiConfig
from app.api.depends import setup_providers
from app.api.middlewares import setup_middlewares
from app.api.routes import setup_routes
from app.common.config.models.paths import Paths
from app.common.config.parser.paths import common_get_paths

logger = logging.getLogger(__name__)


def get_paths() -> Paths:
    return common_get_paths("API_PATH")


def init_api(debug: bool, pool: async_sessionmaker, auth_config: AuthConfig) -> FastAPI:
    logger.debug("Initialize API")
    app = FastAPI(debug=debug, title="FastAPI Template", version="0.0.1", default_response_class=ORJSONResponse)
    setup_middlewares(app)
    setup_providers(app, pool, auth_config)
    setup_routes(app)
    return app


async def run_api(app: FastAPI, api_config: ApiConfig, log_config: str) -> None:
    config = uvicorn.Config(
        app, host=api_config.host,
        port=api_config.port,
        log_level=logging.INFO,
        log_config=log_config
    )
    server = uvicorn.Server(config)
    logger.info("Running API")
    await server.serve()
