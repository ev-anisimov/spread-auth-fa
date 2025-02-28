import copy
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, List

from core.db import get_objects
from spread_auth.models import Entity, EntityObjectType


async def generate_entities(session: AsyncSession, project_id: int, _data: Dict):
    """
    Генерирует и массово сохраняет в БД структуру сущностей на основе входных данных.

    :param session: Асинхронная сессия SQLAlchemy.
    :param project_id: ID проекта.
    :param _data: Входные данные (словарь с locations, subgineries, engineries).
    """
    try:
        engineries = {_['id']: _ for _ in _data['engineries']}
        subgineries = {_['id']: _ for _ in _data['subgineries']}
        _entities = []
        _base = {
            'id':None,
            'project_id': project_id,
            'obj_id': None,
            'obj_type': None,
            'obj_name': None,
            'parent_id': None,
        }
        for _loc_data in _data['locations']:
            _loc_entity = copy.copy(_base)
            _loc_entity['obj_id'] = str(_loc_data['id'])
            _loc_entity['obj_name'] = _loc_data['name']
            _loc_entity['obj_type'] = EntityObjectType.Location
            # _entities.append(_loc_entity)
            _loc = Entity.model_validate(_loc_entity)
            session.add(_loc)
            await session.commit()
            await session.refresh(_loc)
            for _subg_id in _loc_data.get('subgineries', []):
                _subg_data = subgineries.get(_subg_id, {})
                _subg_entity = copy.copy(_base)
                _subg_entity['obj_id'] = str(_subg_data['type'])
                _subg_entity['obj_name'] = _subg_data['name']
                _subg_entity['obj_type'] = EntityObjectType.TypeSubginery
                _subg_entity['parent_id'] = _loc.id
                _sub = Entity.model_validate(_subg_entity)

                session.add(_sub)
                await session.commit()
                await session.refresh(_sub)

                for _eng_id in _subg_data.get('engineries', []):
                    _eng_data = engineries.get(_eng_id, {})

                    _type_eng_entity = copy.copy(_base)
                    _type_eng_entity['obj_id'] = str(_eng_data['type'])
                    _type_eng_entity['obj_name'] = _eng_data['type']
                    _type_eng_entity['obj_type'] = EntityObjectType.TypeEnginery
                    _type_eng_entity['parent_id'] = _sub.id
                    _type_eng = Entity.model_validate(_type_eng_entity)

                    session.add(_type_eng)
                    await session.commit()
                    await session.refresh(_type_eng)

                    _eng_entity = copy.copy(_base)
                    _eng_entity['obj_id'] = str(_eng_data['id'])
                    _eng_entity['obj_name'] = _eng_data['name']
                    _eng_entity['obj_type'] = EntityObjectType.Enginery
                    _eng_entity['parent_id'] = _type_eng.id
                    _eng = Entity.model_validate(_eng_entity)

                    session.add(_eng)
                    await session.commit()
                    await session.refresh(_eng)
    except Exception as ex:
        print(ex)