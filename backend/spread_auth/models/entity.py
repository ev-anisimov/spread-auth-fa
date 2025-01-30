from enum import Enum

from sqlmodel import Field, Relationship
from pydantic import PositiveInt
from spread_auth.models import BaseModelMixin


class EntityObjectType(Enum):
    Location = 'location', 'Location'
    TypeSubginery = 'type_subginery', 'TypeSubginery'
    TypeEnginery = 'type_enginery', 'TypeEnginery'
    Enginery = 'enginery', 'Enginery'


class EntityBase(BaseModelMixin):
    project_id: PositiveInt = Field(default=None, ge=0)
    obj_id: str = Field(max_length=255, nullable=True)
    obj_type: EntityObjectType = Field(max_length=255, nullable=True)
    obj_name: str = Field(max_length=255, nullable=True)
    parent_id: int = Field(foreign_key='entity.id', nullable=True, ondelete='CASCADE')


class Entity(EntityBase, table=True):
    ...