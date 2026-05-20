import time
from django.core.cache import cache

class TokenBucketLimiter:
    def __init__(self, key, capacity, rate):
        self.key = f"ratelimit_{key}"
        self.capacity = capacity
        self.rate = rate
        self.current_tokens = capacity # 初期値を設定

    def is_allowed(self, cost=1.0):
        now = time.time()
        state = cache.get(self.key, {
            "tokens":self.capacity, 
            "last_updated":now
        })

        # 補充計算
        delta_time = now - state["last_updated"]
        new_tokens = min(self.capacity, state["tokens"] + delta_time * self.rate)

        # 判定
        if new_tokens >= cost:
            new_tokens -= cost
            allowed = True
        else:
            allowed = False

        # 最新のトークン数を保持
        self.current_tokens = new_tokens

        # 状態を保存
        cache.set(self.key, {
            "tokens":new_tokens, 
            "last_updated":now
        }, timeout = 600)

        return allowed