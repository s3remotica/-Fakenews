from __future__ import annotations

import ipaddress
import socket
import time
from collections import defaultdict, deque
from urllib.parse import urlparse

from fastapi import HTTPException, Request, status

from .config import settings


class InMemoryRateLimiter:
    def __init__(self, limit_per_minute: int):
        self.limit = limit_per_minute
        self.buckets: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        bucket = self.buckets[key]
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail='Rate limit exceeded. Please wait before retrying.',
            )
        bucket.append(now)


rate_limiter = InMemoryRateLimiter(settings.rate_limit_per_minute)


def rate_limit_dependency(request: Request):
    client_host = request.client.host if request.client else 'unknown'
    rate_limiter.check(client_host)


def validate_safe_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'}:
        raise HTTPException(status_code=400, detail='Only http/https URLs are allowed.')

    try:
        hostname = parsed.hostname
        if not hostname:
            raise HTTPException(status_code=400, detail='Invalid URL host.')

        ip = ipaddress.ip_address(socket.gethostbyname(hostname))
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise HTTPException(status_code=400, detail='Blocked URL host for security reasons.')
    except socket.gaierror as exc:
        raise HTTPException(status_code=400, detail='Unable to resolve URL host.') from exc
