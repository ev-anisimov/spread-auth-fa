from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class BaseModelMixin(SQLModel):
    id: int | None = Field(primary_key=True, index=True)

    updated_at: datetime = Field(nullable=True, default=datetime.now(tz=timezone.utc))


