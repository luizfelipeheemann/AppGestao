from time import time

class AuthRateLimiter:
    def __init__(self, limit=5, interval=60):
        self.attempts = {}
        self.limit = limit
        self.interval = interval

    def is_rate_limited(self, ip: str) -> bool:
        now = time()
        attempts = [t for t in self.attempts.get(ip, []) if now - t < self.interval]
        self.attempts[ip] = attempts
        return len(attempts) >= self.limit

    def record_attempt(self, ip: str):
        self.attempts.setdefault(ip, []).append(time())

auth_rate_limiter = AuthRateLimiter()
