from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql.domain.sql_audio import SqlAudio
from sql.domain.sql_base import SqlBase


class SqlUserAudio(SqlBase):
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(index=True, nullable=False)
    audio_name: Mapped[str] = mapped_column(nullable=False)
    source_id: Mapped[str] = mapped_column(ForeignKey('audio.source_id'), index=True, nullable=False)
    audio: Mapped[SqlAudio] = relationship()
    __tablename__: str = 'user_audio'
