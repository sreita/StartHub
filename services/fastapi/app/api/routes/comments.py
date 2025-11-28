from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.comment import CommentCreate, CommentOut, CommentUpdate
from app.services.comment_service import CommentService

router = APIRouter()


def get_comment_service(db: Session = Depends(get_db)):
    return CommentService(db)


@router.post("/", response_model=CommentOut, status_code=201)
def create_comment(
    payload: CommentCreate,
    user_id: int = Query(..., description="ID del usuario autor"),
    service: CommentService = Depends(get_comment_service),
):
    try:
        return service.create(user_id=user_id, payload=payload)
    except ValueError as e:
        # Entidades relacionadas no encontradas -> 404
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CommentOut])
def list_comments(
    startup_id: int | None = Query(default=None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service: CommentService = Depends(get_comment_service),
):
    return service.list(startup_id, skip=skip, limit=limit)


@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    user_id: int = Query(...),
    service: CommentService = Depends(get_comment_service),
):
    try:
        return service.update(comment_id, user_id, payload)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, user_id: int = Query(...), service: CommentService = Depends(get_comment_service)):
    try:
        service.delete(comment_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None
