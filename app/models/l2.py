from typing import Any, Dict, Optional

from pydantic import BaseModel


class SkillNode(BaseModel):
    user_id: str
    topic: str
    required_level: str
    current_level: str
    gap: str
    signals: Optional[Dict[str, Any]] = None


class SkillNodeUpdate(BaseModel):
    required_level: Optional[str] = None
    current_level: Optional[str] = None
    gap: Optional[str] = None
    signals: Optional[Dict[str, Any]] = None
