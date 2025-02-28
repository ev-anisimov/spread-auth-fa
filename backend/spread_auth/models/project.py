from enum import Enum

from sqlmodel import Field, Relationship, SQLModel
from pydantic import PositiveInt
from spread_auth.models import BaseModelMixin


class ProjectType(str,Enum):
    Spread = 'spread'
    Cloud = 'cloud'
    Custom = 'custom'


class ProjectBase(SQLModel):
    project_id: PositiveInt = Field(default=None, ge=0)
    name: str = Field(max_length=255, unique=True)
    type: ProjectType = Field(default=ProjectType.Spread, nullable=False)
    connection_params: str = Field(default_factory={}, nullable=True)

class ProjectPublic(ProjectBase):
    id: int

class ProjectPublicCount(ProjectPublic):
    cnt: int | None

class Project(BaseModelMixin, ProjectBase, table=True):
    ...