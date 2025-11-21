from sqlalchemy.orm import Session
from . import models, schemas

# --- Read Operations ---

def get_post(db: Session, post_id: int):
    """
    Get a single post by its ID.
    """
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all posts with pagination.
    """
    return db.query(models.Post).offset(skip).limit(limit).all()

# --- Create Operation ---

def create_post(db: Session, post: schemas.PostCreate, author_id: int):
    """
    Create a new post in the database.
    """
    db_post = models.Post(
        title=post.title,
        content=post.content,
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# --- Update Operation ---

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    """
    Update an existing post.
    """
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

# --- Delete Operation ---

def delete_post(db: Session, post_id: int):
    """
    Delete a post from the database.
    """
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    db.delete(db_post)
    db.commit()
    return db_post
