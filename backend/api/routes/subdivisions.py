from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import current_subdivision
from backend.api.schemas import subdivisions as schemas
from backend.api.queries import subdivisions as queries
from backend.api.dependencies import ListPageParams
from backend.settings import LimitOffsetPage
from backend.database import get_db
from backend.models import Subdivision


router = APIRouter(prefix='/subdivisions')


@router.get('/', response_model=LimitOffsetPage[schemas.Subdivision])
def get_subdivisions(params: ListPageParams = Depends(), db: Session = Depends(get_db),):
    return queries.get_subdivisions(db, params)


@router.get('/{subdivision_id}', response_model=schemas.OneSubdivision)
def get_one_subdivision(subdivision: Subdivision = Depends(current_subdivision)):
    return subdivision


@router.post('/', response_model=schemas.OneSubdivision, dependencies=[Depends(admin_only)])
def create_subdivision(subdivision: schemas.CreateSubdivision, db: Session = Depends(get_db)):
    return queries.create_subdivision(db, subdivision)


@router.delete('/{subdivision_id}', status_code=204, dependencies=[Depends(admin_only)])
def delete_subdivision(
    subdivision: Subdivision = Depends(current_subdivision),
    db: Session = Depends(get_db),
):
    queries.delete_subdivision(db, subdivision)
    return {}


@router.patch(
    '/{subdivision_id}',
    response_model=schemas.OneSubdivision,
    dependencies=[Depends(admin_only)],
)
def patch_subdivision(
    subdivision_to_patch: schemas.PatchSubdivision,
    subdivision: Subdivision = Depends(current_subdivision),
    db: Session = Depends(get_db),
):
    return queries.update_subdivision(db, subdivision, subdivision_to_patch)
