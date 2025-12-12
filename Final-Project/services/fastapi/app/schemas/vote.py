from datetime import datetime
from pydantic import BaseModel
from pydantic.config import ConfigDict
from app.models.vote import VoteType


class VoteBase(BaseModel):
    startup_id: int
    vote_type: VoteType


class VoteCreate(VoteBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"startup_id": 1, "vote_type": "upvote"},
                {"startup_id": 1, "vote_type": "downvote"},
            ]
        }
    )


class VoteOut(VoteBase):
    vote_id: int
    user_id: int
    created_date: datetime

    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)


class VoteCount(BaseModel):
    startup_id: int
    upvotes: int
    downvotes: int
