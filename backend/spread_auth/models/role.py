from sqlmodel import Field, Relationship, SQLModel

from spread_auth.models import BaseModelMixin


class RoleBase(SQLModel):
    name: str = Field(max_length=255, unique=True)


class RolePublic(RoleBase):
    id: int


class RolePermissionCnt(RolePublic):
    cnt: int | None

class RolePermission(RolePublic):
    permissions: list | None

class Role(BaseModelMixin, RoleBase, table=True):
    user_roles: list['UserRole'] | None = Relationship(back_populates="role")
    permissions: list['Permission'] | None = Relationship(back_populates="role")
