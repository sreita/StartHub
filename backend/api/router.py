from fastapi import APIRouter
from backend.api.routes import comments, startups, votes, dev, search

api_router = APIRouter()
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(dev.router, prefix="/dev")
api_router.include_router(search.router, prefix="/search-exploration", tags=["search"])
api_router.include_router(startups.router, prefix="/startups", tags=["my_startups"])