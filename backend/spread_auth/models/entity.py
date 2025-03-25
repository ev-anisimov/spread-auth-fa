from enum import Enum

from sqlmodel import Field, Relationship, SQLModel
from pydantic import PositiveInt
from spread_auth.models import BaseModelMixin


class EntityObjectType(Enum):
    Location = 'location'
    TypeSubginery = 'type_subginery'
    TypeEnginery = 'type_enginery'
    Enginery = 'enginery'

    @classmethod
    def get_code_dit_for_upload(cls):
        return {
            cls.Location: ('locationID', int),
            cls.TypeSubginery: ('subgineryType', str),
            cls.TypeEnginery: ('engineryType', str),
            cls.Enginery: ('engineryID', int),

        }

    @classmethod
    def get_code_dict(cls):
        return {
            cls.Location.name: 1,
            cls.TypeSubginery.name: 2,
            cls.TypeEnginery.name: 3,
            cls.Enginery.name: 4,

        }

class EntityBase(SQLModel):
    project_id: PositiveInt = Field(default=None, ge=0)
    obj_id: str = Field(max_length=255, nullable=True)
    obj_type: EntityObjectType = Field(nullable=True)
    obj_name: str = Field(max_length=255, nullable=True)
    parent_id: int|None = Field(foreign_key='entity.id', nullable=True, ondelete='CASCADE')


class Entity(BaseModelMixin, EntityBase, table=True):
    ...