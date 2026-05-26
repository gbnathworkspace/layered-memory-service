import uuid

from app.dal.mongo import get_db
from app.memory.l3.embeddings import embed
from app.models.l3 import EpisodicEntryCreate


async def list_sessions(user_id: str, skip: int, limit: int) -> dict:
    db = get_db()
    total = await db.sessions.count_documents({"user_id": user_id})
    cursor = (
        db.sessions.find({"user_id": user_id}, {"_id": 0, "embedding": 0})
        .sort("date", -1)
        .skip(skip)
        .limit(limit)
    )
    items = await cursor.to_list(length=limit)
    return {"user_id": user_id, "total": total, "skip": skip, "limit": limit, "items": items}


async def save_session(user_id: str, entry: EpisodicEntryCreate) -> str:
    session_id = str(uuid.uuid4())
    vector = await embed(entry.summary)
    doc = {"user_id": user_id, **entry.model_dump(), "session_id": session_id, "embedding": vector}
    await get_db().sessions.insert_one(doc)
    return session_id


async def search_sessions(user_id: str, query: str, k: int = 5) -> list:
    query_vector = await embed(query)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "embedding_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": k * 10,
                "limit": k,
                "filter": {"user_id": user_id},
            }
        },
        {"$project": {"_id": 0, "embedding": 0, "score": {"$meta": "vectorSearchScore"}}},
    ]
    cursor = get_db().sessions.aggregate(pipeline)
    return await cursor.to_list(length=k)


async def delete_session(user_id: str, session_id: str) -> bool:
    result = await get_db().sessions.delete_one({"user_id": user_id, "session_id": session_id})
    return result.deleted_count > 0
