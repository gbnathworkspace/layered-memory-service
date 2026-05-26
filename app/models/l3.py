from typing import Any, Dict, Optional

from pydantic import BaseModel


class EpisodicEntryCreate(BaseModel):
    topic: str
    topic_category: str
    type: str
    date: str
    title: str
    summary: str
    skill_update: Optional[Dict[str, Any]] = None


class EpisodicSearchRequest(BaseModel):
    query: str
    k: int = 5
