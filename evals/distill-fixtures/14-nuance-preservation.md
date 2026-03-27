# Cache Invalidation Strategy

Our caching layer uses a hybrid invalidation approach because no single strategy fits all our data patterns.

**Time-based (TTL):** Product catalog uses a 5-minute TTL. This is acceptable because catalog changes happen via scheduled imports every 6 hours, and a 5-minute staleness window has no measurable impact on conversion rates. We tested 1-minute, 5-minute, and 15-minute TTLs in A/B tests (N=45,000 sessions each, February 2026): conversion rates were 3.42%, 3.41%, and 3.39% respectively — not statistically significant (p=0.87).

**Event-driven:** User profile and cart data invalidate immediately on write via Redis pub/sub. This is necessary because stale cart data causes checkout failures — we measured a 2.1% failure rate before implementing event-driven invalidation (now 0.02%).

**Version-based:** API responses include an `ETag` header. Clients with stale ETags get fresh data; clients with current ETags get 304 Not Modified. This saves approximately 340GB/day of bandwidth (measured over January 2026, averaging 42 million API calls/day, average response size 8.1KB).

The hybrid approach adds complexity (three invalidation paths to maintain), but the alternative — a single TTL for everything — would force a tradeoff between freshness (cart data) and efficiency (catalog data) that our A/B tests showed is unnecessary.

One genuine limitation: during the 6-hourly catalog import, there's a 30-second window where the cache and database are inconsistent even with event-driven invalidation, because the import is a bulk operation that doesn't trigger individual write events. We accept this because it affects only the import window and the 5-minute TTL self-corrects shortly after.
