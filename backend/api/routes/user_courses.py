from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import current_user
from backend.api.errors.errors import bad_request, not_found
from backend.models.users import User
from backend.database import get_db
from backend.api.queries import courses, user_courses as queries
from backend.api.schemas import user_courses as schemas
from backend.api.dependencies import ListPageParams
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/user/{user_id}/courses')


def user_himself_only(
    user_id: int,
    user: User = Depends(current_user),
):
    if user_id != user.id:
        raise not_found()


@router.get('/', response_model=LimitOffsetPage[schemas.NamedUserCourse], dependencies=[Depends(user_himself_only)])
def get_user_courses(
    user_id: int,
    params: ListPageParams = Depends(),
    db: Session = Depends(get_db)
):
    return queries.get_user_courses(db, user_id, params)


@router.get('/{course_id}', response_model=schemas.OneUserCourse, dependencies=[Depends(user_himself_only)])
def get_one_user_course(
    course_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    user_course = queries.get_annotated_user_course_by_course_id(db, course_id, user_id)
    if user_course is None:
        raise not_found()
    return user_course


@router.post('/', response_model=schemas.UserCourse, dependencies=[Depends(user_himself_only)])
def create_user_course(course_data: schemas.CreateCourse,
                       user_id: int,
                       user: User = Depends(current_user),
                       db: Session = Depends(get_db)):
    if queries.get_user_course_by_course_id(db, course_data.course_id, user_id) is not None:
        raise bad_request("User is already registered for this course")
    course = courses.get_course(db, course_data.course_id)
    if course is None:
        raise not_found()
    return queries.create_user_course(db, user, course)


@router.delete('/{course_id}', status_code=204, dependencies=[Depends(user_himself_only)])
def delete_user_course(course_id: int,
                       user: User = Depends(current_user),
                       db: Session = Depends(get_db)):
    user_course = queries.get_user_course_by_course_id(db, course_id, user.id)
    if user_course is None:
        raise not_found()
    queries.delete_user_course(db, user_course)
    return {}
