from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db
from ..auth import get_current_user, User

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_new_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new post.
    The author_id is taken from the authenticated user's ID.
    """
    return crud.create_post(db=db, post=post, author_id=current_user.id)

@router.get("/", response_model=List[schemas.Post])
def read_all_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all posts.
    This endpoint does not require authentication.
    """
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
def read_single_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single post by its ID.
    This endpoint does not require authentication.
    """
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=schemas.Post)
def update_existing_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a post.
    Requires authentication and checks for post ownership.
    """
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
        
    return crud.update_post(db=db, post_id=post_id, post_update=post_update)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a post.
    Requires authentication and checks for post ownership.
    """
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
        
    crud.delete_post(db=db, post_id=post_id)
    return {"message": "Post deleted successfully"}

