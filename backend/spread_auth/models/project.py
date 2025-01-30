from enum import Enum

from sqlmodel import Field, Relationship
from pydantic import PositiveInt
from spread_auth.models import BaseModelMixin


class ProjectType(Enum):
    Spread = 'spread', 'Spread'
    Cloud = 'cloud', 'Cloud'
    Custom = 'custom', 'Custom'


class ProjectBase(BaseModelMixin):
    project_id: PositiveInt = Field(default=None, ge=0)
    name: str = Field(max_length=255, unique=True)
    type: ProjectType = Field(default=ProjectType.Spread, nullable=False)
    connection_params: str = Field(default_factory={}, nullable=True)


class Project(ProjectBase, table=True):
    ...