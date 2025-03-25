import copy
from collections import defaultdict
from itertools import product
from typing import Dict, List

from sqlmodel import select, distinct
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text

from spread_auth.core.cache import PermissionUsersCache
from spread_auth.core.db import get_objects, async_session
from spread_auth.models import User, Permission,Entity, EntityObjectType, Role, UserRole


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
            'id': None,
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


def _exists_in_hierarchy(_hierarchy, nodes):
    for node in nodes:
        if node == '*':
            continue
        if node in _hierarchy.get(nodes.index(node) + 1):
            return True
        break
    return False


async def get_entities_ancestors_hierarchy(session: AsyncSession, project, obj_id, obj_type):
    query = text('''
        WITH RECURSIVE Ancestors AS (
          SELECT id, obj_id, parent_id, obj_name, obj_type, cast(id as text) as hierarhy_id
          FROM entity
          WHERE obj_id = :obj_id AND obj_type::VARCHAR = :obj_type AND project_id = :project
          UNION ALL
          SELECT pe.id, pe.obj_id, pe.parent_id, pe.obj_name, pe.obj_type, a.hierarhy_id||'.'||pe.id as hierarhy_id
          FROM entity pe
          JOIN Ancestors a ON pe.id = a.parent_id
        )
        SELECT *
        FROM Ancestors
        ORDER BY parent_id;
    ''').bindparams(obj_id=obj_id, obj_type=obj_type, project=project)
    res = await session.execute(query)
    return res.all()


async def check_permission(session: AsyncSession, all_perms, project: int, obj_id: str, obj_type: str):
    """
    Получение результирующего(по всей иерархии) модификатора доступа по конкретному ограничению
    @param project: идентификатор проекта
    @param obj_id: идентификатор оборудования
    @param obj_type: тип оборудования
    @return: число - модификатор доступа AccessType: Full = 0, 'Полный доступ'
                                                     Read = 1, 'Просмотр'
                                                     Denied = 2, 'Доступ запрещен'
    """
    db_hierarchy = await get_entities_ancestors_hierarchy(session, project, obj_id, obj_type)

    _obj_types = EntityObjectType.get_code_dict()
    _perms = []
    # TODO: здесь в иерархии теряется узел, если например инжененрный объект в двух локациях
    _hierarchy = defaultdict(set)
    # _hierarchy = {_obj_types[h.obj_type]: h.obj_id for h in hierarchy}
    for h in db_hierarchy:
        _hierarchy[_obj_types[h.obj_type]].add(h.obj_id)
    for _code_index, obj_id in _hierarchy.items():
        for perm in all_perms:
            perm_parts = perm.code.split('/')
            pp = perm_parts[_code_index]
            if pp in obj_id and all(_ == '*' for _ in perm_parts[_code_index + 1:]):
                if _exists_in_hierarchy(_hierarchy, perm_parts[1:]):
                    _perms.append(perm)
            # if entity.obj_id == pp and not perm_parts[_code_index + 1:]:
            #     _perms.append(perm)
    [_perms.append(perm) for perm in all_perms if perm.code == f'{project}/*/*/*/*']
    return max(_perms, key=lambda x: x.index).access if _perms else 2


async def get_permission_for_user(session: AsyncSession, _user: User, _project: int):
    _obj_types = EntityObjectType.get_code_dit_for_upload()
    _roles = await get_objects(session, Role, [UserRole.user_id == _user.id], [UserRole], limit=None)
    _roles = [_role.id for _role in _roles]
    _all_entities = await get_objects(session, Entity, [Entity.project_id==_project], limit=None)
    all_perms = await get_objects(session, Permission,
                                  [Permission.project==_project, Permission.role_id.in_(_roles)], limit=None,
                                  order=['role_id', 'index'])
    entity_dict = {entity.id: entity for entity in _all_entities}
    access_rights = {0: 'Editor',
                     1: 'Reviewer',
                     2: "None"}
    # 0 Editor - Полный доступ, 1 Reviewer - Просмотр, 2 None - Доступ запрещен
    tree = []
    for entity in _all_entities:
        node = {
            _obj_types[entity.obj_type][0]: _obj_types[entity.obj_type][1](entity.obj_id),
            "accessRights": access_rights[await check_permission(session, all_perms, _project, entity.obj_id, str(entity.obj_type.name))]
        }
        if entity.parent_id is not None:
            parent = entity_dict[entity.parent_id]
            if 'constraints' not in parent:
                parent['constraints'] = []
            parent['constraints'].append(node)
        else:
            tree.append(node)
        entity_dict[entity.id] = node
    return {"constraints": tree}


async def fill_cache_permission_for_users():
    async with async_session() as session:
        _all_users = await get_objects(session, User, limit=None)
        _all_projects = await session.exec(select(distinct(Permission.project)))
        _all_projects = _all_projects.all()
        _cache = PermissionUsersCache()
        for _user, _project in product(_all_users, _all_projects):
            _cache.set(f'{_user.id}/{_project}', await get_permission_for_user(session, _user, _project))