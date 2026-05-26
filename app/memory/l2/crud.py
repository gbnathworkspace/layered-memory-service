from app.dal.mongo import get_db
from app.models.l2 import SkillNode, SkillNodeUpdate


async def get_all_skills(user_id: str) -> list:
    cursor = get_db().skill_graph.find({"user_id": user_id}, {"_id": 0})
    return await cursor.to_list(length=None)


async def get_skill(user_id: str, topic: str):
    return await get_db().skill_graph.find_one({"user_id": user_id, "topic": topic}, {"_id": 0})


async def create_skill(node: SkillNode) -> str:
    await get_db().skill_graph.insert_one(node.model_dump())
    return node.topic


async def update_skill(user_id: str, topic: str, update: SkillNodeUpdate) -> bool:
    fields = {k: v for k, v in update.model_dump().items() if v is not None}
    result = await get_db().skill_graph.update_one(
        {"user_id": user_id, "topic": topic}, {"$set": fields}
    )
    return result.matched_count > 0


async def delete_skill(user_id: str, topic: str) -> bool:
    result = await get_db().skill_graph.delete_one({"user_id": user_id, "topic": topic})
    return result.deleted_count > 0
