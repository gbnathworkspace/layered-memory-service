from fastapi import APIRouter, Depends, HTTPException

from app.core.security import verify_api_key
from app.memory.l1.crud import create_profile, delete_profile, get_profile, update_profile
from app.models.l1 import CoreProfile, CoreProfileUpdate

router = APIRouter(
    prefix="/memory/profile",
    tags=["L1 Profile"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/{user_id}")
async def fetch_profile(user_id: str):
    doc = await get_profile(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


@router.post("", status_code=201)
async def create(profile: CoreProfile):
    user_id = await create_profile(profile)
    return {"user_id": user_id}


@router.put("/{user_id}")
async def update(user_id: str, body: CoreProfileUpdate):
    ok = await update_profile(user_id, body)
    if not ok:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"updated": True}


@router.delete("/{user_id}", status_code=204)
async def delete(user_id: str):
    ok = await delete_profile(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Profile not found")
