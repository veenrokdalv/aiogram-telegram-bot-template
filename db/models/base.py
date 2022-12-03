import sqlalchemy
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id = sqlalchemy.Column(
        sqlalchemy.BigInteger(),
        autoincrement=True,
        primary_key=True,
        unique=True,
        nullable=False,
    )

    def __str__(self):
        return f'<{self.__name__}({self.id})>'


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime(),
        server_default=sqlalchemy.func.now(),
    )
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime(),
        server_default=sqlalchemy.func.now(),
        server_onupdate=sqlalchemy.func.now(),
    )

    def __str__(self):
        return f'<{self.__name__}({self.id} {self.created_date} {self.modified_date})>'
