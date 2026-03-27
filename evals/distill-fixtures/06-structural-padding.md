# Environment Variables

## Introduction

This document describes the environment variables used by our application. Below you will find a comprehensive guide to all configuration options.

## Table of Contents

- [Database](#database)
- [Redis](#redis)
- [API Keys](#api-keys)
- [Feature Flags](#feature-flags)

---

## Database

### Database Connection

| Variable | Description |
|----------|-------------|
| `DB_HOST` | Database hostname |
| `DB_PORT` | Database port (default: 5432) |

### Database Pool Settings

- **`DB_POOL_MIN`**: Minimum pool connections (default: 5)
- **`DB_POOL_MAX`**: Maximum pool connections (default: 20)

---

## Redis

### Redis Connection

> Redis is used for caching and session storage.

- **`REDIS_URL`**: Redis connection URL (default: `redis://localhost:6379`)

---

## API Keys

### External Service API Keys

The following API keys are required:

1. **`STRIPE_SECRET_KEY`**: Stripe payment processing key
2. **`SENDGRID_API_KEY`**: SendGrid email service key
3. **`SENTRY_DSN`**: Sentry error tracking DSN

---

## Feature Flags

### Application Feature Flags

| Flag | Default | Description |
|------|---------|-------------|
| `FF_NEW_CHECKOUT` | `false` | Enables new checkout flow |
| `FF_DARK_MODE` | `true` | Enables dark mode option |

---

## Summary

This document covered all environment variables for database, Redis, API keys, and feature flags configuration. Refer to this guide when setting up new environments.
