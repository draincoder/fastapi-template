import asyncio
import logging

from sqlalchemy.orm import close_all_sessions

from app.api.config.parser.main import load_app_config
from app.api.main_factory import get_paths, run_api, init_api
from app.common.config.parser import setup_logging
from app.infrastructure.db.factory import create_engine, create_session_maker

logger = logging.getLogger(__name__)


async def main() -> None:
    paths = get_paths()

    setup_logging(paths)
    config = load_app_config(paths)
    engine = create_engine(config.db)
    pool = create_session_maker(engine)
    app = init_api(config.api.debug, pool, config.auth)
    logger.info("Started")
    try:
        await run_api(app, config.api, str(paths.logging_config_file))
    finally:
        close_all_sessions()
        await engine.dispose()
        logger.info("Stopped")


if __name__ == '__main__':
    asyncio.run(main())
