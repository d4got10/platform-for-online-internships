from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel
from backend.models import User, Competence


class UserCompetence(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    competence_id = Column(Integer, ForeignKey(Competence.id), nullable=False, index=True)

    user: Mapped[User] = relationship(primaryjoin=user_id == User.id, back_populates='user_competencies')
    competence: Mapped[Competence] = relationship(primaryjoin=competence_id == Competence.id)

    __table_args__ = (
        UniqueConstraint(user_id, competence_id, name='u_competencies_per_user'),
    )
