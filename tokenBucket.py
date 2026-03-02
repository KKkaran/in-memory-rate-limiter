import time
from typing import Dict


class TokenBucketRateLimiting:
    def __init__(self, capacity:int, refillRate:int) -> None:
        self.capacity =  capacity
        self.refillRate = refillRate
        self._users: Dict[str, dict] = {}


    def make_request(self, user_id):
        now = time.time()
        if not user_id in self._users:
            self._users[user_id] = {
                "last_refill_request":now,
                "remaining_tokens": self.capacity
            }

        user_state = self._users[user_id]

        user_state["remaining_tokens"] = min(self.capacity, (now - user_state["last_refill_request"]) * self.refillRate) + user_state["remaining_tokens"]
        user_state["last_refill_request"] = now

        # print(user_state["count"])
        if user_state["remaining_tokens"] >= 1:
            user_state["remaining_tokens"] -= 1
            return True

        return False



tokenRl = TokenBucketRateLimiting(5, 1)

for index in range(8): #without sleep, this shows requests made instantly, 5 return True, 3 False
    print(tokenRl.make_request('user-1'))
    # time.sleep(1)
print()

print('waiting 2 s')
time.sleep(2) # sleep for 2s, gives 2 tokens

print()
for index in range(5): # 2 return True, 3 False
    print(tokenRl.make_request('user-1'))


