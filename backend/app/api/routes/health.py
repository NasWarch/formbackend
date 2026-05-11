"""Health check endpoint — vérifie DB + Redis."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from redis import ConnectionError as RedisConnectionError

from app.core.database import get_db
from app.core.redis import get_redis

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Vérifie la connectivité base de données et Redis."""
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    redis_ok = False
    redis_client = get_redis()
    if redis_client:
        try:
            redis_client.ping()
            redis_ok = True
        except RedisConnectionError:
            pass

    return {
        "status": "ok" if db_ok and redis_ok else "degraded",
        "db": db_ok,
        "redis": redis_ok,
    }
