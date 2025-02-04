from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class BaseModelMixin(SQLModel):
    id: int | None = Field(primary_key=True, index=True)

    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(tz=timezone.utc).replace(tzinfo=None)  # Убираем tzinfo
    )


