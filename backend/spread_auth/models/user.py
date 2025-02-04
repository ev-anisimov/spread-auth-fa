from sqlmodel import Field, Relationship, SQLModel

from pydantic import computed_field

from spread_auth.models import BaseModelMixin


class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True, max_length=150)
    first_name: str | None  = Field(nullable=True, unique=False, max_length=150)
    last_name: str | None  = Field(nullable=True, unique=False, max_length=150)
    is_service: bool | None  = Field(nullable=True, default=False)
    is_staff: bool | None  = Field(nullable=True, default=False)

    @computed_field
    @property
    def name(self) -> str:
        return self.first_name + " " + self.last_name


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]


class User(BaseModelMixin, UserBase, table=True):
    password: str
    user_roles: list['UserRole'] | None = Relationship(back_populates="user")
