from app.database.base import Base
from app.database.session import engine
from app.models import user, document  # noqa: F401 - import to register models


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
