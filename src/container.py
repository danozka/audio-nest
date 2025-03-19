import logging
import logging.config

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Resource
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.services.i_users_repository import IUsersRepository
from audio_nest.services.i_videos_repository import IVideosRepository
from audio_nest.use_cases.videos_getter import VideosGetter
from authentication.authentication_service import AuthenticationService
from authentication.json_web_token_handler import JsonWebTokenHandler
from settings import Settings
from sql.sql_session_maker_handler import handle_sql_session_maker
from sql.sql_users_repository import SqlUsersRepository
from youtube.youtube_videos_repository import YoutubeVideosRepository


class Container(DeclarativeContainer):
    # Configuration
    configuration: Configuration = Configuration(pydantic_settings=[Settings()])

    # Resources
    logging: Resource[None] = Resource(logging.config.dictConfig, config=configuration.logging_config)
    sql_session_maker: Resource[async_sessionmaker[AsyncSession]] = Resource(
        handle_sql_session_maker,
        database_path=configuration.database_path
    )

    # Services
    users_repository: Factory[IUsersRepository] = Factory(SqlUsersRepository, sql_session_maker=sql_session_maker)
    videos_repository: Factory[IVideosRepository] = Factory(
        YoutubeVideosRepository,
        max_results=configuration.youtube_search_max_results
    )

    # Authentication
    json_web_token_handler: Factory[JsonWebTokenHandler] = Factory(
        JsonWebTokenHandler,
        secret_key=configuration.json_web_token_secret_key,
        algorithm=configuration.json_web_token_algorithm,
        expiration_days=configuration.json_web_token_expiration_days
    )
    authentication_service: Factory[AuthenticationService] = Factory(
        AuthenticationService,
        json_web_token_handler=json_web_token_handler,
        users_repository=users_repository
    )

    # Use cases
    videos_getter: Factory[VideosGetter] = Factory(VideosGetter, videos_repository=videos_repository)
