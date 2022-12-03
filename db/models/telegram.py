import sqlalchemy

from db.models.base import TimedBaseModel


class TelegramUser(TimedBaseModel):
    __tablename__ = 'telegram_users'

    username = sqlalchemy.Column(
        sqlalchemy.String(length=32),
        nullable=True,
        index=True,
    )

    first_name = sqlalchemy.Column(
        sqlalchemy.String(length=64),
        nullable=False,
        index=True,
    )

    last_name = sqlalchemy.Column(
        sqlalchemy.String(length=64),
        nullable=True,
        index=True,
    )
