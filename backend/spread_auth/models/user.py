from sqlmodel import Field, Relationship

from pydantic import computed_field

from spread_auth.models import BaseModelMixin


class UserBase(BaseModelMixin):
    username: str = Field(nullable=False, unique=True, max_length=150)
    first_name: str = Field(nullable=True, unique=False, max_length=150)
    last_name: str = Field(nullable=True, unique=False, max_length=150)
    is_service: bool = Field(nullable=True, default=False)
    is_staff: bool = Field(nullable=True, default=False)

    @computed_field
    @property
    def name(self) -> str:
        return self.first_name + " " + self.last_name


class UserPublic(UserBase):
    hashed_password: str


class User(UserBase, table=True):
    password: str
    user_roles: list['UserRole'] | None = Relationship(back_populates="user")
