from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class SqlAlchemyBase(MappedAsDataclass, DeclarativeBase):
    pass
