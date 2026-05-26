from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.limiter import limiter
from app.core.security import verify_api_key
from app.memory.l3.crud import delete_session, list_sessions, save_session, search_sessions
from app.models.l3 import EpisodicEntryCreate, EpisodicSearchRequest

router = APIRouter(
    prefix="/memory/episodic",
    tags=["L3 Episodic"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/{user_id}")
async def list_episodes(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await list_sessions(user_id, skip, limit)


@router.post("/{user_id}", status_code=201)
async def save_episode(user_id: str, entry: EpisodicEntryCreate):
    session_id = await save_session(user_id, entry)
    return {"session_id": session_id}


@router.post("/{user_id}/search")
@limiter.limit("20/minute")
async def search_episodes(request: Request, user_id: str, body: EpisodicSearchRequest):
    return await search_sessions(user_id, body.query, body.k)


@router.delete("/{user_id}/{session_id}", status_code=204)
async def delete_episode(user_id: str, session_id: str):
    ok = await delete_session(user_id, session_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
