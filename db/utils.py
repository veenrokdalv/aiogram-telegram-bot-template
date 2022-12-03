import os
from importlib import import_module

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from config import settings


def get_db_url(driver='asyncpg') -> str:
    url = (
        f'postgresql+{driver}://{settings.POSTGRES_USER}:'
        f'{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:'
        f'{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}'
    )
    return url


def registry_models():
    models_dir = settings.BASE_DIR / 'db' / 'models'
    exclude_modules = ('base.py', '__init__.py')

    for filename in os.listdir(models_dir):
        if not filename.endswith('.py') or filename in exclude_modules:
            continue
        import_module(f'db.models.{filename[:-3]}')


def setup() -> tuple[AsyncEngine, AsyncSession]:
    registry_models()

    url = get_db_url()

    db_engine = create_async_engine(url=url)
    db_session = async_sessionmaker(bind=db_engine)
    return db_engine, db_session
