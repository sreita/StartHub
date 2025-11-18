from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.vote import VoteCreate, VoteOut, VoteCount
from backend.services.vote_service import VoteService

router = APIRouter()


def get_vote_service(db: Session = Depends(get_db)):
    return VoteService(db)


@router.post("/", response_model=VoteOut)
def upsert_vote(payload: VoteCreate, user_id: int = Query(...), response: Response = None, service: VoteService = Depends(get_vote_service)):
    try:
        vote, created = service.upsert(user_id, payload)
        if created and response is not None:
            # Devolver 201 en creación; FastAPI serializa con VoteOut
            response.status_code = 201
        return vote
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/count/{startup_id}", response_model=VoteCount)
def count_votes(startup_id: int, service: VoteService = Depends(get_vote_service)):
    return service.count(startup_id)


@router.delete("/", status_code=204)
def delete_vote(user_id: int = Query(...), startup_id: int = Query(...), service: VoteService = Depends(get_vote_service)):
    try:
        service.delete(user_id=user_id, startup_id=startup_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None
