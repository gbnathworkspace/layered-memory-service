from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from app.dal.mongo import get_db

router = APIRouter(
    prefix="/memory/user",
    tags=["User"],
    dependencies=[Depends(verify_api_key)],
)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    db = get_db()
    async with await db.client.start_session() as session:
        async with session.start_transaction():
            await db.profiles.delete_many({"user_id": user_id}, session=session)
            await db.skill_graph.delete_many({"user_id": user_id}, session=session)
            await db.sessions.delete_many({"user_id": user_id}, session=session)
