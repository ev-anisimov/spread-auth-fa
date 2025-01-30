from sqlmodel import Field, Relationship

from spread_auth.models import BaseModelMixin


class RoleBase(BaseModelMixin):
    name: str = Field(max_length=255, unique=True)


class Role(RoleBase, table=True):
    user_roles: list['UserRole'] | None = Relationship(back_populates="role")
    permissions: list['Permission'] | None = Relationship(back_populates="role")
