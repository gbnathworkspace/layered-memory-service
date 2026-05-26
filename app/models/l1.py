from typing import Optional

from pydantic import BaseModel


class CoreProfile(BaseModel):
    user_id: str
    goal: str
    deadline: str
    overall_level: str
    daily_availability: str
    email: str


class CoreProfileUpdate(BaseModel):
    goal: Optional[str] = None
    deadline: Optional[str] = None
    overall_level: Optional[str] = None
    daily_availability: Optional[str] = None
    email: Optional[str] = None
