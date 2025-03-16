from sqlalchemy.orm import Mapped, mapped_column

from sql_alchemy_persistence.domain.sql_alchemy_base import SqlAlchemyBase


class SqlAlchemyUser(SqlAlchemyBase):
    id: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    email: Mapped[str] = mapped_column(index=True, nullable=False, repr=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False, repr=False)
    __tablename__: str = 'users'
