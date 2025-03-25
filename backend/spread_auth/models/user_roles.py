from sqlmodel import Field, Relationship, SQLModel

from spread_auth.models import BaseModelMixin, User, Role


class UserRoleBase(SQLModel):
    user_id: int = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    role_id: int = Field(default=None, foreign_key="role.id", ondelete="CASCADE")


class UserRole(BaseModelMixin, UserRoleBase, table=True):
    user: User | None = Relationship(back_populates="user_roles")
    role: Role | None = Relationship(back_populates="user_roles")
    # updated_at: datetime = Field(nullable=True, default=datetime.now(tz=timezone.utc))
