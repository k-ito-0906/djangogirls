import time
from django.core.cache import cache

class TokenBucketLimiter:
    def __init__(self, key, capacity, rate):
        self.key = f"ratelimit_{key}"
        self.capacity = capacity
        self.rate = rate

    def is_allowed(self):
        now = time.time()
        state = cache.get(self.key, {
            "tokens":self.capacity, 
            "last_updated":now
        })

        #補充計算
        delta_time = now - state["last_updated"]#前回アクセスからの経過時間
        new_tokens = min(self.capacity, state["tokens"] + delta_time * self.rate)

        #判定
        if new_tokens >= 1.0:
            new_tokens -=1.0
            allowed = True
        else:
            allowed = False

        #状態を保存
        cache.set(self.key, {
            "tokens":new_tokens, 
            "last_updated":now
        }, timeout = 600) #10分間アクセスがなければ破棄

        return allowed