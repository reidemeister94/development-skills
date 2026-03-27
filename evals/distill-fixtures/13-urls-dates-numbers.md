# Release Notes v3.2.0

It's worth mentioning that this release was deployed on March 1, 2026 at 14:00 UTC. The deployment was managed by Sarah Chen (@schen) and reviewed by Marco Rossi (@mrossi).

## New Features

Furthermore, the following features have been added:

- **WebSocket support** — Real-time notifications via `wss://api.example.com/ws`. Documentation: https://docs.example.com/websocket. Jira: PLAT-4521.
- **Bulk import API** — POST `/api/v2/import/bulk` accepts up to 10,000 records per request. Throughput: 847 records/second. Memory: 256MB max per batch. Jira: PLAT-4498.
- **SSO integration** — SAML 2.0 via Okta. Config: https://admin.example.com/sso/configure. Contact: security@example.com for SAML metadata. Jira: SEC-892.

## Bug Fixes

Additionally, it should be noted that the following bugs were fixed:

- Fixed race condition in order processing that caused duplicate charges for 0.3% of transactions (approximately $12,400 in duplicates since January 15, 2026). Jira: BUG-7891. Hotfix applied: February 22, 2026 at 09:15 UTC.
- Fixed memory leak in image resizer: RSS growth from 512MB to 4.2GB over 72 hours. Root cause: unclosed file descriptors in the libvips binding. Jira: BUG-7903.
- Fixed timezone handling: `America/Chicago` and `America/Denver` were swapped in the dropdown, affecting 2,847 users. Jira: BUG-7910.

## Performance

In terms of performance improvements, response times improved:

| Endpoint | Before | After | Improvement |
|----------|--------|-------|-------------|
| GET /api/orders | 340ms p99 | 89ms p99 | -73.8% |
| POST /api/checkout | 1,200ms p99 | 450ms p99 | -62.5% |
| GET /api/products | 180ms p99 | 42ms p99 | -76.7% |

## Known Issues

- PLAT-4530: WebSocket reconnection fails after exactly 3,600 seconds (1 hour) due to token expiration. Workaround: refresh token at 3,500s. Fix ETA: March 8, 2026.
- BUG-7915: PDF export truncates tables wider than 210mm (A4 width). No workaround. Fix ETA: v3.2.1.
