from datetime import datetime
from backend.api.schemas.base import BaseSchema


class UserCourse(BaseSchema):
    id: int
    user_id: int
    course_id: int
    progress: float
    admission_date: datetime


class NamedUserCourse(UserCourse):
    course_name: str


class OneUserCourse(NamedUserCourse):
    course_description: str


class CreateCourse(BaseSchema):
    course_id: int
