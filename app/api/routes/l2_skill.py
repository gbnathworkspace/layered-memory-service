from fastapi import APIRouter, Depends, HTTPException

from app.core.security import verify_api_key
from app.memory.l2.crud import create_skill, delete_skill, get_all_skills, get_skill, update_skill
from app.models.l2 import SkillNode, SkillNodeUpdate

router = APIRouter(
    prefix="/memory/skill",
    tags=["L2 Skill Graph"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/{user_id}")
async def fetch_all(user_id: str):
    return await get_all_skills(user_id)


@router.get("/{user_id}/{topic}")
async def fetch_one(user_id: str, topic: str):
    doc = await get_skill(user_id, topic)
    if not doc:
        raise HTTPException(status_code=404, detail="Skill node not found")
    return doc


@router.post("/{user_id}", status_code=201)
async def create(user_id: str, node: SkillNode):
    topic = await create_skill(node)
    return {"topic": topic}


@router.put("/{user_id}/{topic}")
async def update(user_id: str, topic: str, body: SkillNodeUpdate):
    ok = await update_skill(user_id, topic, body)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill node not found")
    return {"updated": True}


@router.delete("/{user_id}/{topic}", status_code=204)
async def delete(user_id: str, topic: str):
    ok = await delete_skill(user_id, topic)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill node not found")
