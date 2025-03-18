import logging
import logging.config

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Resource
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.persistence.i_users_repository import IUsersRepository
from authentication.authentication_service import AuthenticationService
from authentication.json_web_token_handler import JsonWebTokenHandler
from settings import Settings
from sql_alchemy_persistence.sql_alchemy_session_maker_handler import handle_session_maker
from sql_alchemy_persistence.sql_alchemy_users_repository import SqlAlchemyUsersRepository


class Container(DeclarativeContainer):
    configuration: Configuration = Configuration(pydantic_settings=[Settings()])
    logging: Resource[None] = Resource(logging.config.dictConfig, config=configuration.logging_config)
    session_maker: Resource[async_sessionmaker[AsyncSession]] = Resource(
        handle_session_maker,
        database_path=configuration.database_path
    )
    json_web_token_handler: Factory[JsonWebTokenHandler] = Factory(
        JsonWebTokenHandler,
        secret_key=configuration.json_web_token_secret_key,
        algorithm=configuration.json_web_token_algorithm,
        expiration_days=configuration.json_web_token_expiration_days
    )
    users_repository: Factory[IUsersRepository] = Factory(SqlAlchemyUsersRepository, session_maker=session_maker)
    authentication_service: Factory[AuthenticationService] = Factory(
        AuthenticationService,
        json_web_token_handler=json_web_token_handler,
        users_repository=users_repository
    )
