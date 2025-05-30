from sqlalchemy.orm import Mapped, mapped_column

from sql.domain.sql_base import SqlBase


class SqlUser(SqlBase):
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    __tablename__: str = 'users'
