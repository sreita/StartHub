from fastapi import APIRouter
from backend.api.routes import comments, votes, dev

api_router = APIRouter()
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(dev.router, prefix="/dev")
