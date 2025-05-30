from sqlalchemy.orm import Mapped, mapped_column

from sql.domain.sql_base import SqlBase


class SqlAudio(SqlBase):
    source_id: Mapped[str] = mapped_column(primary_key=True)
    file_path: Mapped[str] = mapped_column(nullable=False)
    bit_rate_kbps: Mapped[int] = mapped_column(nullable=False)
    codec: Mapped[str] = mapped_column(nullable=False)
    __tablename__: str = 'audio'
