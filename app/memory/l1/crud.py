from app.dal.mongo import get_db
from app.models.l1 import CoreProfile, CoreProfileUpdate


async def get_profile(user_id: str):
    return await get_db().profiles.find_one({"user_id": user_id}, {"_id": 0})


async def create_profile(profile: CoreProfile) -> str:
    await get_db().profiles.insert_one(profile.model_dump())
    return profile.user_id


async def update_profile(user_id: str, update: CoreProfileUpdate) -> bool:
    fields = {k: v for k, v in update.model_dump().items() if v is not None}
    result = await get_db().profiles.update_one({"user_id": user_id}, {"$set": fields})
    return result.matched_count > 0


async def delete_profile(user_id: str) -> bool:
    result = await get_db().profiles.delete_one({"user_id": user_id})
    return result.deleted_count > 0
