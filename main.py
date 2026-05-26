from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import l1_profile, l2_skill, l3_episodic, user
from app.core.limiter import limiter
from app.dal.mongo import close_db, connect_db

app = FastAPI(title="Layered Memory Service")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)

app.include_router(l1_profile.router)
app.include_router(l2_skill.router)
app.include_router(l3_episodic.router)
app.include_router(user.router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
