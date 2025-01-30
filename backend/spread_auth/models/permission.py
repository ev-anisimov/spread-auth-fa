from datetime import datetime, timezone
from enum import IntEnum

from sqlmodel import Field, SQLModel, Relationship
from pydantic import PositiveInt

from spread_auth.models import BaseModelMixin, Role


class AccessType(IntEnum):
    Full = 0  # Полный доступ
    Read = 1  # Просмотр
    Denied = 2  # Доступ запрещен


class PermissionBase(BaseModelMixin):
    role_id: int = Field(foreign_key='role.id', ondelete="CASCADE")
    project: PositiveInt = Field(default=None, ge=0)
    code: str = Field(default=None, nullable=False, max_length=255)
    access: AccessType = Field(default=AccessType.Full, nullable=True)
    index: int = Field(default=0, nullable=True)
    invalid: bool = Field(default=False)
    is_deleted: bool = Field(default=False)


class Permission(PermissionBase, table=True):
    role: Role | None = Relationship(back_populates="permissions")
