# API Rate Limiting Configuration

It's important to note that our API rate limiting system currently utilizes a token bucket algorithm. It's worth mentioning that each authenticated user is allocated 1000 requests per hour. It should be noted that unauthenticated requests are limited to 100 per hour.

It bears mentioning that when a client exceeds their rate limit, the server returns a 429 status code. As you may know, the response includes a `Retry-After` header indicating how many seconds to wait. Needless to say, clients should implement exponential backoff.

As mentioned earlier, the rate limits are configurable via environment variables:

```
RATE_LIMIT_AUTH=1000
RATE_LIMIT_ANON=100
RATE_LIMIT_WINDOW=3600
```

Keep in mind that these values apply per-user, not per-IP. One could argue that IP-based limiting would be more effective against abuse, but the team decided user-based limiting better serves our legitimate API consumers.
