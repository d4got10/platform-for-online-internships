from operator import attrgetter
from typing import Callable, TypeVar
from sqlalchemy import func, or_, and_, Column, cast, String
from sqlalchemy.orm import Query, Session
from backend.api.errors.errors import bad_request
from backend.models.base import BaseModel


T = TypeVar('T')
TModel = TypeVar('TModel', bound=BaseModel)


def with_search(*fields: Column, query: Query[T], search: str | None) -> Query[T]:
    if search:
        filters = [
            func.lower(cast(field, String)).like(f'%{search.lower()}%')
            for field in fields
        ]
        query = query.filter(or_(*filters))
    return query


def get_instances_or_400(db: Session, model: TModel, ids: list[int]) -> list[TModel]:
    instances = []
    if ids:
        instances = db.query(model).filter(model.id.in_(ids)).all()
    if len(ids) != len(instances):
        raise bad_request('Some of the instances not exist.')
    return instances


def sort_by_self_fk(objects: Query[TModel] | list[TModel], attr_: str) -> list[TModel]:
    if isinstance(objects, Query):
        objects = objects.all()

    objects = list(objects)

    if not objects:
        return objects

    cur = None
    firsts = [item for item in objects if getattr(item, attr_) is None]
    if firsts:
        cur = firsts[0]
    else:
        cur = min(objects, key=attrgetter(attr_))

    result = [cur]
    objects.remove(cur)
    while len(objects) > 0:
        for obj in objects:
            if getattr(obj, attr_) == cur.id:
                cur = obj
                result.append(cur)
                objects.remove(obj)

    return result


def create_with_respect_to_prev_instance(
    *,
    db: Session,
    create_data: dict,
    prev_id_attr_name: str,
    next_instance_attr_name: str,
    model: type[BaseModel],
    get_first_func: Callable,
    get_prev_func: Callable,
):
    def after_add_callback(created_instance):
        pass

    if create_data[prev_id_attr_name] is None:
        existing_first = get_first_func()
        if existing_first is not None:

            def callback(created_instance):
                setattr(existing_first, prev_id_attr_name, created_instance.id)

            after_add_callback = callback  # noqa: F811
    else:
        existing_prev = get_prev_func()
        if existing_prev is None:
            raise bad_request(
                f'Instance with id {create_data[prev_id_attr_name]} does not exist.'
            )

        def callback(created_instance):
            next_instance = getattr(existing_prev, next_instance_attr_name)
            if next_instance is not None:
                setattr(next_instance, prev_id_attr_name, created_instance.id)
            setattr(created_instance, prev_id_attr_name, existing_prev.id)

        after_add_callback = callback

    create_data.pop(prev_id_attr_name, None)
    created_instance = model(**create_data)

    db.add(created_instance)
    db.commit()
    db.refresh(created_instance)

    after_add_callback(created_instance)
    db.commit()
    db.refresh(created_instance)

    return created_instance


def update_with_respect_to_prev_instance(
    *,
    db: Session,
    instance: BaseModel,
    update_data: dict,
    prev_id_attr_name: str,
    next_instance_attr_name: str,
    additional_filters_to_search_for_instance_to_update: list | None = None,
):
    instance_to_update = None
    additional_filters_to_search_for_instance_to_update = \
        additional_filters_to_search_for_instance_to_update or []

    def after_update_callback(instance_to_update, prev_instance_id):
        pass

    if prev_id_attr_name in update_data:
        prev_instance_id_to_set = update_data.pop(prev_id_attr_name)
        if getattr(instance, prev_id_attr_name) != prev_instance_id_to_set:

            if getattr(instance, next_instance_attr_name) is not None:
                next_instance = getattr(instance, next_instance_attr_name)
                setattr(next_instance, prev_id_attr_name, getattr(instance, prev_id_attr_name))

            model = type(instance)
            instance_to_update = db.query(model).filter(and_(
                getattr(model, prev_id_attr_name) == prev_instance_id_to_set,
                *additional_filters_to_search_for_instance_to_update,
            )).one_or_none()
            setattr(instance, prev_id_attr_name, prev_instance_id_to_set)

            if instance_to_update is not None:
                setattr(instance_to_update, prev_id_attr_name, None)

                def callback(instance_to_update, prev_instance_id):
                    setattr(instance_to_update, prev_id_attr_name, prev_instance_id)

                after_update_callback = callback  # noqa: F811

    for key, value in update_data.items():
        setattr(instance, key, value)

    db.commit()
    db.refresh(instance)

    after_update_callback(instance_to_update, instance.id)
    db.commit()

    return instance


def delete_with_respect_to_prev_instance(
    *,
    db: Session,
    instance: BaseModel,
    prev_id_attr_name: str,
    next_instance_attr_name: str,
):
    next_instance = getattr(instance, next_instance_attr_name)
    prev_id = getattr(instance, prev_id_attr_name)

    db.delete(instance)
    db.commit()

    if next_instance is not None:
        setattr(next_instance, prev_id_attr_name, prev_id)

    db.commit()
