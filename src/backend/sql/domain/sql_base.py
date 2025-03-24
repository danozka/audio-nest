from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class SqlBase(MappedAsDataclass, DeclarativeBase):
    pass
