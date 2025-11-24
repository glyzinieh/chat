from sqlmodel import SQLModel, create_engine

from .core.config import settings

if settings.DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(settings.DATABASE_URL)
