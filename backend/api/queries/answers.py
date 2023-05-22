from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.api.schemas import answers as schemas
from backend.models.answers import Answer


def get_answers(db: Session, task_id: int, params: ListPageParams) -> List[Answer]:
    query = db.query(Answer).filter(Answer.task_id == task_id)
    return paginate(query, params)


def get_answer(db: Session, answer_id) -> Answer | None:
    return db.query(Answer).get(answer_id)


def create_answer(db: Session, answer: schemas.CreateAnswer, task_id: int) -> Answer:
    answer = Answer(**answer.dict())
    answer.task_id = task_id
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def delete_answer(db: Session, answer: Answer):
    db.delete(answer)
    db.commit()


def patch_answer(db: Session, answer: Answer, data: schemas.PatchAnswer) -> Answer:
    db.query(Answer).filter(Answer.id == answer.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(answer)
    return answer