from sqlalchemy.orm import Session, load_only, joinedload
from fastapi_pagination.ext.sqlalchemy import paginate
from backend.api.dependencies import ListPageParams, PostsListPageParams
from backend.models import Post, Course, Competence, User
from backend.models.association_tables import UserPostAssociation
from backend.api.schemas import posts as schemas
from backend.api.queries.helpers import get_instances_or_400, with_search


def get_posts(db: Session, params: PostsListPageParams):
    query = db.query(Post).options(load_only(Post.id, Post.name, Post.subdivision_id))
    if params.subdivision_id:
        query = query.filter(Post.subdivision_id == params.subdivision_id)
    query = with_search(Post.name, query=query, search=params.search)
    return paginate(query, params)


def get_posts_by_subdivision_id(db: Session, subdivision_id: int, params: ListPageParams):
    query = db.query(Post).filter(Post.subdivision_id == subdivision_id).options(load_only(
        Post.id,
        Post.name,
    ))
    query = with_search(Post.name, query=query, search=params.search)
    return paginate(query, params)


def get_post(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def create_post(db: Session, post: schemas.CreateSubdivisionPost, subdivision_id: int):
    created_post = Post(subdivision_id=subdivision_id, **post.dict(exclude={'courses', 'competencies'}))
    created_post.courses = get_instances_or_400(db, Course, post.courses)
    created_post.competencies = get_instances_or_400(db, Competence, post.competencies)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()


def update_post(db: Session, post: Post, patch_data: schemas.PatchSubdivisionPost):
    dict_ = patch_data.dict(exclude_unset=True)
    if 'courses' in dict_:
        post.courses = get_instances_or_400(db, Course, dict_.pop('courses'))
    if 'competencies' in dict_:
        post.competencies = get_instances_or_400(db, Competence, dict_.pop('competencies'))
    for key, value in dict_.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


def get_mastered_posts(db: Session, intern: User):
    user_post_ids = db.query(UserPostAssociation.c.post_id).filter(
        UserPostAssociation.c.user_id == intern.id,
    )
    user_competencies = set(intern.competencies)
    user_posts = db.query(Post).filter(
        Post.id.in_(user_post_ids),
    ).options(
        joinedload(Post.competencies),
    )

    return [
        post for post in user_posts.all()
        if set(post.competencies).issubset(user_competencies)
    ]
