import logging
import logging.config

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Resource
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.services.i_audio_repository import IAudioRepository
from audio_nest.services.i_audio_sources_repository import IAudioSourcesRepository
from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from audio_nest.services.i_users_repository import IUsersRepository
from audio_nest.use_cases.audio_getter import AudioGetter
from audio_nest.use_cases.audio_sources_getter import AudioSourcesGetter
from audio_nest.use_cases.user_audio_adder import UserAudioAdder
from authentication.authentication_service import AuthenticationService
from authentication.json_web_token_handler import JsonWebTokenHandler
from settings import Settings
from sql.sql_session_maker_handler import handle_sql_session_maker
from sql.sql_user_audio_repository import SqlUserAudioRepository
from sql.sql_users_repository import SqlUsersRepository
from youtube.youtube_audio_repository import YoutubeAudioRepository
from youtube.youtube_audio_sources_repository import YoutubeAudioSourcesRepository


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
    audio_repository: Factory[IAudioRepository] = Factory(
        YoutubeAudioRepository,
        bit_rate_kbps=configuration.audio_bit_rate_kbps,
        codec=configuration.audio_codec,
        ffmpeg_path=configuration.ffmpeg_path,
        download_directory_path=configuration.audio_directory_path
    )
    audio_sources_repository: Factory[IAudioSourcesRepository] = Factory(
        YoutubeAudioSourcesRepository,
        max_results=configuration.youtube_search_max_results
    )
    user_audio_repository: Factory[IUserAudioRepository] = Factory(
        SqlUserAudioRepository,
        sql_session_maker=sql_session_maker
    )
    users_repository: Factory[IUsersRepository] = Factory(SqlUsersRepository, sql_session_maker=sql_session_maker)

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
    audio_getter: Factory[AudioGetter] = Factory(AudioGetter, audio_repository=audio_repository)
    audio_sources_getter: Factory[AudioSourcesGetter] = Factory(
        AudioSourcesGetter,
        audio_sources_repository=audio_sources_repository
    )
    user_audio_adder: Factory[UserAudioAdder] = Factory(UserAudioAdder, user_audio_repository=user_audio_repository)
