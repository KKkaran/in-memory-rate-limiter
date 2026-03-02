import time
from typing import Dict

# this is rate limting at the application level, /user, /api-key
class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, interval_seconds: int):
        self.max_requests = max_requests
        self.interval = interval_seconds
        self._users: Dict[str, dict] = {}

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()

        # Initialize state if first request
        if user_id not in self._users:
            self._users[user_id] = {
                "window_start": now,
                "count": 0
            }

        user_state = self._users[user_id]

        # Check if window expired
        if now - user_state["window_start"] >= self.interval:
            user_state["window_start"] = now
            user_state["count"] = 0

        # Enforce limit
        if user_state["count"] < self.max_requests:
            user_state["count"] += 1
            return True

        return False



rl = FixedWindowRateLimiter(max_requests=5, interval_seconds=5)

for i in range(12):
    allowed = rl.is_allowed(f"user")
    print(f"Request {i+1}: {allowed}")
    time.sleep(0.5)