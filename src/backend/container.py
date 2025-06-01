import logging
import logging.config

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Resource
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.use_cases.audio_getter import AudioGetter
from audio_nest.use_cases.audio_sources_getter import AudioSourcesGetter
from audio_nest.use_cases.user_audio_adder import UserAudioAdder
from audio_nest.use_cases.user_audio_deleter import UserAudioDeleter
from audio_nest.use_cases.user_audio_getter import UserAudioGetter
from audio_nest.use_cases.user_audio_list_getter import UserAudioListGetter
from auth.services.json_web_token_handler import JsonWebTokenHandler
from auth.use_cases.user_getter import UserGetter
from auth.use_cases.user_login_handler import UserLoginHandler
from auth.use_cases.user_registration_handler import UserRegistrationHandler
from settings import Settings
from sql.sql_audio_repository import SqlAudioRepository
from sql.sql_session_maker_handler import handle_sql_session_maker
from sql.sql_user_audio_repository import SqlUserAudioRepository
from sql.sql_users_repository import SqlUsersRepository
from youtube.youtube_audio_downloader import YoutubeAudioDownloader
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
    audio_downloader: Factory[YoutubeAudioDownloader] = Factory(
        YoutubeAudioDownloader,
        bit_rate_kbps=configuration.audio_bit_rate_kbps,
        codec=configuration.audio_codec,
        ffmpeg_path=configuration.ffmpeg_path,
        download_directory_path=configuration.audio_directory_path
    )
    audio_repository: Factory[SqlAudioRepository] = Factory(SqlAudioRepository, sql_session_maker=sql_session_maker)
    audio_sources_repository: Factory[YoutubeAudioSourcesRepository] = Factory(
        YoutubeAudioSourcesRepository,
        max_results=configuration.youtube_search_max_results
    )
    json_web_token_handler: Factory[JsonWebTokenHandler] = Factory(
        JsonWebTokenHandler,
        secret_key=configuration.json_web_token_secret_key,
        algorithm=configuration.json_web_token_algorithm,
        expiration_days=configuration.json_web_token_expiration_days
    )
    user_audio_repository: Factory[SqlUserAudioRepository] = Factory(
        SqlUserAudioRepository,
        sql_session_maker=sql_session_maker
    )
    users_repository: Factory[SqlUsersRepository] = Factory(SqlUsersRepository, sql_session_maker=sql_session_maker)

    # Use cases
    audio_getter: Factory[AudioGetter] = Factory(
        AudioGetter,
        audio_downloader=audio_downloader,
        audio_repository=audio_repository
    )
    audio_sources_getter: Factory[AudioSourcesGetter] = Factory(
        AudioSourcesGetter,
        audio_sources_repository=audio_sources_repository
    )
    user_audio_adder: Factory[UserAudioAdder] = Factory(UserAudioAdder, user_audio_repository=user_audio_repository)
    user_audio_deleter: Factory[UserAudioDeleter] = Factory(
        UserAudioDeleter,
        user_audio_repository=user_audio_repository
    )
    user_audio_getter: Factory[UserAudioGetter] = Factory(UserAudioGetter, user_audio_repository=user_audio_repository)
    user_audio_list_getter: Factory[UserAudioListGetter] = Factory(
        UserAudioListGetter,
        user_audio_repository=user_audio_repository
    )
    user_getter: Factory[UserGetter] = Factory(
        UserGetter,
        users_repository=users_repository,
        json_web_token_handler=json_web_token_handler
    )
    user_login_handler: Factory[UserLoginHandler] = Factory(
        UserLoginHandler,
        users_repository=users_repository,
        json_web_token_handler=json_web_token_handler
    )
    user_registration_handler: Factory[UserRegistrationHandler] = Factory(
        UserRegistrationHandler,
        users_repository=users_repository
    )
