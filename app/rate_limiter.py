from __future__ import annotations

import time
import uuid

from fastapi import HTTPException

WINDOW_SECONDS = 60


class RateLimiter:
    def __init__(self, client, limit_per_minute: int) -> None:
        self.client = client
        self.limit = limit_per_minute

    @staticmethod
    def _key(user_id: str) -> str:
        return f"ratelimit:{user_id}"

    def hit_count(self, user_id: str, now: float | None = None) -> int:
        now = time.time() if now is None else now
        key = self._key(user_id)
        self.client.zremrangebyscore(key, 0, now - WINDOW_SECONDS)
        return self.client.zcard(key)

    def check(self, user_id: str, now: float | None = None) -> None:
        now = time.time() if now is None else now
        if self.hit_count(user_id, now) >= self.limit:
            raise HTTPException(
                status_code=429,
                detail="rate limit exceeded",
                headers={"Retry-After": str(WINDOW_SECONDS)},
            )

        key = self._key(user_id)
        self.client.zadd(key, {f"{now}:{uuid.uuid4().hex}": now})
        self.client.expire(key, WINDOW_SECONDS)
