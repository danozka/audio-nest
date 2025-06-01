import logging
from contextlib import asynccontextmanager
from logging import Logger
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import routers
from api.routers import auth, sources, user_audio
from container import Container


class App(FastAPI):
    _log: Logger = logging.getLogger(__name__)
    _container: Container

    def __init__(self, container: Container) -> None:
        self._container = container
        self._container.wire(packages=[routers])
        super().__init__(
            openapi_url=None,
            docs_url=None,
            redoc_url= None,
            swagger_ui_oauth2_redirect_url=None,
            lifespan=self._handle_resources,
        )
        self.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        self.include_router(auth.router)
        self.include_router(sources.router)
        self.include_router(user_audio.router)

    def run(self) -> None:
        uvicorn.run(
            app=self,
            host=self._container.configuration.app_host(),
            port=self._container.configuration.app_port(),
            log_config=self._container.configuration.logging_config()
        )

    @asynccontextmanager
    async def _handle_resources(self, app: FastAPI) -> AsyncGenerator[None, None]:
        self._log.info('Initializing application resources...')
        await self._container.sql_session_maker.init()
        yield
        self._log.info('Shutting down application resources...')
        await self._container.sql_session_maker.shutdown()
        self._log.info('Application resources shut down')
