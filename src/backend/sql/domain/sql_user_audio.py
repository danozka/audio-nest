from sqlalchemy.orm import Mapped, mapped_column

from sql.domain.sql_base import SqlBase


class SqlUserAudio(SqlBase):
    id: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    user_id: Mapped[str] = mapped_column(nullable=False)
    audio_name: Mapped[str] = mapped_column(nullable=False)
    source_id: Mapped[str] = mapped_column(index=True, nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    bit_rate_kbps: Mapped[int] = mapped_column(nullable=False)
    codec: Mapped[str] = mapped_column(nullable=False)
    __tablename__: str = 'user_audio'
