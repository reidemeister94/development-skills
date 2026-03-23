# API Endpoint Documentation Template

Use this template for each API endpoint file in `docs/workflows/api/{method}-{path-slug}.md`.

**CRITICAL**: This documentation must allow someone to **reimplement the endpoint from scratch** without looking at the code. Every validation rule, every business decision, every error case must be documented.

---

## Naming Convention

File names follow pattern: `{method}-{path-slug}.md`

Examples:
- `GET /api/users` → `get-api-users.md`
- `POST /api/orders` → `post-api-orders.md`
- `GET /api/users/:id` → `get-api-users-id.md`
- `DELETE /api/orders/:id/items/:itemId` → `delete-api-orders-id-items-itemid.md`

---

## Template Structure

```markdown
# {METHOD} {/path}

> **Source**: `{file.py}:{line_number}`
> **Handler Function**: `{function_name}()`
> **Router Registration**: `{router_file.py}:{line}`
> **Added**: {version/date} by {author}
> **Last Modified**: {date} - {reason}

## Purpose

{Comprehensive explanation of what this endpoint does and WHY it exists. Not just "returns users" but the full business context.}

**Business Context**:
- WHO uses this endpoint? (frontend, mobile app, external partners, internal services)
- WHEN is it called? (user action, background job, scheduled task)
- WHAT problem does it solve?
- WHAT would break if this endpoint didn't exist?

**Example Use Cases**:
1. User opens the dashboard → frontend calls this to load initial data
2. Mobile app pulls to refresh → calls this with `since` parameter for incremental update
3. Admin searches for a user → calls this with `q` parameter

## Authentication & Authorization

### Authentication

| Aspect | Value | Details |
|--------|-------|---------|
| **Required** | Yes/No | If No, explain why (public endpoint) |
| **Method** | Bearer JWT / API Key / Session | How token is passed |
| **Token Location** | `Authorization` header / Cookie / Query param | Exact location |
| **Validation** | `auth_middleware.py:45` | Where token is validated |

**Token Validation Process** (step by step):
1. Extract token from `Authorization: Bearer {token}` header (`middleware.py:12`)
2. Decode JWT using `JWT_SECRET` env var (`auth.py:34`)
3. Check `exp` claim - reject if expired with `401 TOKEN_EXPIRED`
4. Check `iss` claim matches our issuer - reject with `401 INVALID_TOKEN`
5. Load user from `users` table by `sub` claim (`user_repository.py:56`)
6. If user not found or `status != 'active'`, reject with `401 USER_INACTIVE`
7. Attach user object to request context for handler use

### Authorization

| Check | Implementation | Failure Response |
|-------|----------------|------------------|
| Role required | `@require_role('admin')` decorator | `403 {"error": "FORBIDDEN", "message": "Admin role required"}` |
| Resource ownership | Handler checks `resource.user_id == current_user.id` | `403 {"error": "FORBIDDEN", "message": "Not your resource"}` |
| Feature flag | `if not feature_enabled('new_dashboard', user)` | `403 {"error": "FEATURE_DISABLED"}` |

**Authorization Logic in Detail**:
```python
# From {file.py}:{lines}
# Step 1: Check role (decorator runs before handler)
if 'admin' not in current_user.roles:
    raise ForbiddenError("Admin role required")

# Step 2: Check resource ownership (inside handler)
order = get_order(order_id)
if order.user_id != current_user.id and 'admin' not in current_user.roles:
    raise ForbiddenError("Cannot access other user's orders")

# Step 3: Check organization access (multi-tenant)
if order.org_id != current_user.org_id:
    raise ForbiddenError("Cannot access other organization's data")
```

## Request Specification

### URL Pattern

```
{METHOD} {/full/path/:with/:params}?{query_params}
```

**Example URLs**:
```
GET /api/users/123?include=orders&fields=name,email
GET /api/users?status=active&page=2&per_page=50
POST /api/users
```

### Path Parameters

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `id` | integer | positive int | Yes | User's unique identifier (database PK) |
| `orderId` | string | UUID v4 | Yes | Order's public identifier |

**Path Parameter Validation** (`validators.py:23`):
- `id`: Must be positive integer. Regex: `^\d+$`. Invalid → `400 INVALID_PATH_PARAM`
- `orderId`: Must be valid UUID v4. Invalid → `400 INVALID_UUID`

### Query Parameters

| Parameter | Type | Required | Default | Validation | Description |
|-----------|------|----------|---------|------------|-------------|
| `page` | integer | No | 1 | min=1 | Page number for pagination |
| `per_page` | integer | No | 20 | min=1, max=100 | Results per page |
| `status` | string | No | (all) | enum: active,inactive,deleted | Filter by status |
| `q` | string | No | - | min_length=2, max_length=100 | Search query (searches name, email) |
| `sort` | string | No | created_at | enum: created_at,name,email | Sort field |
| `order` | string | No | desc | enum: asc,desc | Sort direction |
| `include` | string | No | - | comma-separated: orders,profile,roles | Related data to include |
| `fields` | string | No | (all) | comma-separated field names | Sparse fieldset |
| `since` | ISO datetime | No | - | ISO 8601 format | Return only records modified after this time |

**Query Parameter Details**:

#### `q` (Search Query)
- **Minimum length**: 2 characters (to avoid expensive full-table scans)
- **Search targets**: `users.name`, `users.email` using PostgreSQL `ILIKE`
- **Search query built**: `WHERE name ILIKE '%{q}%' OR email ILIKE '%{q}%'`
- **Performance note**: Uses `pg_trgm` index for queries ≥3 chars, falls back to sequential for 2 chars
- **Special characters**: `%` and `_` are escaped before use in LIKE

#### `include` (Eager Loading)
- **Purpose**: Reduce N+1 queries by specifying related data upfront
- **Allowed values**: `orders`, `profile`, `roles`, `recent_activity`
- **Invalid value handling**: Silently ignored (no error)
- **SQL impact**: Adds JOINs to main query

```sql
-- Without include
SELECT * FROM users WHERE id = 123;
-- Then N additional queries for orders

-- With include=orders
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.id = 123;
```

#### `fields` (Sparse Fieldset)
- **Purpose**: Reduce response payload size
- **Allowed fields**: Any field in `UserPublicSchema` (name, email, status, created_at, etc.)
- **Always included**: `id`, `type` (even if not requested)
- **Invalid field handling**: Silently ignored

### Request Headers

| Header | Required | Format | Description |
|--------|----------|--------|-------------|
| `Authorization` | Yes | `Bearer {jwt}` | Authentication token |
| `Content-Type` | Yes* | `application/json` | *Required for POST/PUT/PATCH |
| `Accept` | No | `application/json` | Response format (only JSON supported) |
| `X-Request-ID` | No | UUID | Client-provided request ID for tracing |
| `X-Idempotency-Key` | No* | string | *Recommended for POST to prevent duplicates |

### Request Body (POST/PUT/PATCH)

```json
{
  "name": "John Doe",           // Required, string, 1-200 chars
  "email": "john@example.com",  // Required, valid email format
  "password": "secret123",      // Required for POST, optional for PATCH, min 8 chars
  "role": "user",               // Optional, enum: user|admin|moderator, default: user
  "metadata": {                 // Optional, object
    "timezone": "America/New_York",
    "locale": "en-US",
    "notifications": {
      "email": true,
      "push": false
    }
  },
  "tags": ["vip", "beta"]       // Optional, array of strings, max 10 items
}
```

#### Field-by-Field Validation

| Field | Type | Required | Validation Rules | Error Code |
|-------|------|----------|------------------|------------|
| `name` | string | Yes | min=1, max=200, no HTML tags | `INVALID_NAME` |
| `email` | string | Yes | RFC 5322 format, max=255, unique in DB | `INVALID_EMAIL`, `EMAIL_EXISTS` |
| `password` | string | Yes (POST) | min=8, must contain letter+number | `WEAK_PASSWORD` |
| `role` | string | No | enum: user,admin,moderator | `INVALID_ROLE` |
| `metadata` | object | No | max depth=3, max size=10KB | `INVALID_METADATA` |
| `tags` | array | No | max 10 items, each max 50 chars | `TOO_MANY_TAGS` |

#### Validation Implementation (`validators.py:67-120`)

```python
def validate_create_user(data: dict) -> dict:
    errors = []

    # Name validation
    name = data.get('name', '').strip()
    if not name:
        errors.append({"field": "name", "code": "REQUIRED"})
    elif len(name) > 200:
        errors.append({"field": "name", "code": "TOO_LONG", "max": 200})
    elif contains_html(name):
        errors.append({"field": "name", "code": "INVALID_NAME", "message": "HTML not allowed"})

    # Email validation
    email = data.get('email', '').strip().lower()
    if not email:
        errors.append({"field": "email", "code": "REQUIRED"})
    elif not is_valid_email(email):
        errors.append({"field": "email", "code": "INVALID_EMAIL"})
    elif user_repository.exists_by_email(email):
        errors.append({"field": "email", "code": "EMAIL_EXISTS"})

    # Password validation (required for POST, optional for PATCH)
    password = data.get('password')
    if password is not None:  # Only validate if provided
        if len(password) < 8:
            errors.append({"field": "password", "code": "TOO_SHORT", "min": 8})
        elif not re.search(r'[a-zA-Z]', password) or not re.search(r'\d', password):
            errors.append({"field": "password", "code": "WEAK_PASSWORD",
                          "message": "Must contain letter and number"})

    if errors:
        raise ValidationError(errors)

    return {
        "name": name,
        "email": email,
        "password_hash": hash_password(password) if password else None,
        "role": data.get('role', 'user'),
        "metadata": data.get('metadata', {}),
        "tags": data.get('tags', [])[:10]  # Silently truncate to 10
    }
```

## Response Specification

### Success Response

**Status Code**: `200 OK` (GET, PATCH) | `201 Created` (POST) | `204 No Content` (DELETE)

**Response Headers**:
| Header | Value | Description |
|--------|-------|-------------|
| `Content-Type` | `application/json` | Response format |
| `X-Request-ID` | `{uuid}` | Request ID for tracing (echoes client ID or generates new) |
| `X-RateLimit-Limit` | `1000` | Requests allowed per hour |
| `X-RateLimit-Remaining` | `999` | Requests remaining |
| `X-RateLimit-Reset` | `1642531200` | Unix timestamp when limit resets |

**Response Body**:

```json
{
  "data": {
    "id": 123,
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "status": "active",
      "role": "user",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T15:45:00Z"
    },
    "relationships": {
      "orders": {
        "links": {
          "related": "/api/users/123/orders"
        },
        "meta": {
          "count": 5
        }
      }
    },
    "meta": {
      "last_login_at": "2024-01-20T14:00:00Z"
    }
  },
  "included": [
    // Only present if ?include=orders
    {
      "id": 456,
      "type": "order",
      "attributes": {
        "total": 99.99,
        "status": "completed"
      }
    }
  ],
  "meta": {
    "request_id": "abc-123-def"
  }
}
```

**For list endpoints** (GET /api/users):

```json
{
  "data": [
    { "id": 1, "type": "user", "attributes": {...} },
    { "id": 2, "type": "user", "attributes": {...} }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 156,
      "total_pages": 8
    },
    "request_id": "abc-123-def"
  },
  "links": {
    "self": "/api/users?page=1&per_page=20",
    "first": "/api/users?page=1&per_page=20",
    "prev": null,
    "next": "/api/users?page=2&per_page=20",
    "last": "/api/users?page=8&per_page=20"
  }
}
```

### Response Field Reference

| Field Path | Type | Always Present | Description |
|------------|------|----------------|-------------|
| `data` | object/array | Yes | Main payload |
| `data.id` | integer | Yes | Resource identifier |
| `data.type` | string | Yes | Resource type name |
| `data.attributes.name` | string | Yes | User's display name |
| `data.attributes.email` | string | Depends on permissions | Email (hidden for non-admin viewing others) |
| `data.attributes.status` | string | Yes | active, inactive, deleted |
| `data.attributes.created_at` | ISO datetime | Yes | When created |
| `data.meta.last_login_at` | ISO datetime | If available | Last login timestamp (null if never logged in) |
| `meta.pagination` | object | List endpoints only | Pagination info |
| `included` | array | Only if `?include` used | Related resources |

### Fields NOT Included (Security)

These fields exist in the database but are NEVER returned by this endpoint:

| Field | Reason | Where to access |
|-------|--------|-----------------|
| `password_hash` | Security - never expose | N/A |
| `internal_notes` | Admin-only data | Admin API |
| `ip_address` | Privacy | Audit logs |
| `raw_metadata` | Contains PII | N/A |

### Error Responses

#### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "code": "INVALID_EMAIL",
        "message": "Invalid email format"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Password must be at least 8 characters",
        "min": 8
      }
    ],
    "request_id": "abc-123-def"
  }
}
```

#### Complete Error Catalog

| Status | Code | Message | When | Resolution |
|--------|------|---------|------|------------|
| 400 | `VALIDATION_ERROR` | "Invalid input" | Request body fails validation | Check `details` array for specific fields |
| 400 | `INVALID_JSON` | "Malformed JSON" | Request body is not valid JSON | Fix JSON syntax |
| 400 | `MISSING_BODY` | "Request body required" | POST/PUT without body | Include JSON body |
| 401 | `UNAUTHORIZED` | "Authentication required" | No token provided | Include `Authorization` header |
| 401 | `TOKEN_EXPIRED` | "Token has expired" | JWT `exp` claim in past | Refresh token |
| 401 | `INVALID_TOKEN` | "Invalid token" | Token signature invalid | Re-authenticate |
| 403 | `FORBIDDEN` | "Access denied" | User lacks permission | Check user's role/permissions |
| 403 | `RATE_LIMITED` | "Too many requests" | Rate limit exceeded | Wait for `X-RateLimit-Reset` |
| 404 | `NOT_FOUND` | "User not found" | ID doesn't exist or soft-deleted | Verify ID is correct |
| 409 | `CONFLICT` | "Email already exists" | Unique constraint violation | Use different email |
| 422 | `UNPROCESSABLE` | "Cannot delete user with orders" | Business rule violation | Cancel orders first |
| 500 | `INTERNAL_ERROR` | "Internal server error" | Unexpected exception | Contact support with request_id |
| 503 | `SERVICE_UNAVAILABLE` | "Database unavailable" | Dependency down | Retry later |

## Handler Implementation

### Complete Code Walkthrough

```python
# File: api/users.py
# Lines: 45-120

@router.get("/api/users/{user_id}")
@require_auth
@rate_limit(limit=1000, period=3600)
async def get_user(
    user_id: int,
    include: str = None,
    fields: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single user by ID.

    Permissions:
    - Users can view their own profile
    - Admins can view any user
    - Some fields hidden for non-owners
    """

    # Step 1: Validate path parameter
    # user_id already validated as int by FastAPI/Pydantic
    if user_id < 1:
        raise HTTPException(400, {"code": "INVALID_ID"})

    # Step 2: Fetch user from database
    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at.is_(None)  # Exclude soft-deleted
    ).first()

    if not user:
        raise HTTPException(404, {"code": "NOT_FOUND", "message": "User not found"})

    # Step 3: Authorization check
    is_own_profile = user.id == current_user.id
    is_admin = 'admin' in current_user.roles

    if not is_own_profile and not is_admin:
        # Non-admins can only view their own profile
        raise HTTPException(403, {"code": "FORBIDDEN", "message": "Cannot view other users"})

    # Step 4: Build response based on permissions
    response_data = {
        "id": user.id,
        "type": "user",
        "attributes": {
            "name": user.name,
            "status": user.status,
            "created_at": user.created_at.isoformat(),
        }
    }

    # Email: visible to self and admins only
    if is_own_profile or is_admin:
        response_data["attributes"]["email"] = user.email

    # Role: visible to admins only
    if is_admin:
        response_data["attributes"]["role"] = user.role
        response_data["meta"] = {
            "internal_id": user.internal_id,  # Admin-only field
            "last_login_ip": user.last_login_ip
        }

    # Step 5: Handle includes (eager loading)
    if include:
        includes_list = [i.strip() for i in include.split(',')]
        included = []

        if 'orders' in includes_list:
            orders = db.query(Order).filter(Order.user_id == user.id).limit(10).all()
            for order in orders:
                included.append({
                    "id": order.id,
                    "type": "order",
                    "attributes": {
                        "total": float(order.total),
                        "status": order.status
                    }
                })
            response_data["relationships"] = {
                "orders": {"meta": {"count": len(orders)}}
            }

        if included:
            response_data["included"] = included

    # Step 6: Apply sparse fieldset
    if fields:
        allowed_fields = set(fields.split(','))
        response_data["attributes"] = {
            k: v for k, v in response_data["attributes"].items()
            if k in allowed_fields or k in ('id', 'type')  # Always include id, type
        }

    return {"data": response_data}
```

### Key Decision Points Explained

#### Why check `deleted_at.is_(None)`?
- We use soft deletes for users (GDPR compliance, audit trail)
- Soft-deleted users should not appear in API responses
- This is the standard pattern across all user-related queries

#### Why separate permission levels for email?
- Privacy: Users shouldn't see each other's email addresses
- But admins need it for support purposes
- This follows GDPR principle of data minimization

#### Why limit included orders to 10?
- Prevent accidentally loading thousands of orders
- If user needs all orders, they should use `/api/users/{id}/orders` endpoint
- Includes are for convenience preview, not full data access

## Database Interactions

### Queries Executed

#### Main User Query

```sql
-- Always executed
SELECT
    id, name, email, status, role, created_at, updated_at,
    deleted_at, internal_id, last_login_ip
FROM users
WHERE id = :user_id
  AND deleted_at IS NULL
LIMIT 1;
```

**Index used**: `PRIMARY KEY (id)`
**Typical execution time**: <1ms

#### Orders Include Query (conditional)

```sql
-- Only if ?include=orders
SELECT
    id, user_id, total, status, created_at
FROM orders
WHERE user_id = :user_id
ORDER BY created_at DESC
LIMIT 10;
```

**Index used**: `idx_orders_user_id_created`
**Typical execution time**: 1-5ms depending on order count

### Database State Changes (for POST/PUT/DELETE)

| Operation | Tables Modified | Trigger Side Effects |
|-----------|-----------------|---------------------|
| POST (create) | `users` INSERT | `audit_log` INSERT via trigger |
| PATCH (update) | `users` UPDATE | `updated_at` auto-set, `audit_log` INSERT |
| DELETE (soft) | `users` UPDATE (`deleted_at`) | No cascade (soft delete) |

## Side Effects

### For State-Changing Operations (POST/PUT/DELETE)

| Side Effect | When | Implementation |
|-------------|------|----------------|
| Audit log entry | Always | DB trigger on `users` table |
| Cache invalidation | Always | `cache.delete(f"user:{user_id}")` after commit |
| Email notification | User creation | Queued to `notifications` service via Redis |
| Webhook | If configured | POST to `webhooks.user.created` subscribers |
| Analytics event | Always | Fire-and-forget to analytics service |

### Cache Behavior

| Cache Key | TTL | Invalidated On |
|-----------|-----|----------------|
| `user:{id}` | 5 min | Update, Delete |
| `users:list:{hash}` | 1 min | Any user change |
| `users:count:{filters}` | 1 min | Create, Delete |

## Rate Limiting

| Limit Type | Value | Scope | Headers |
|------------|-------|-------|---------|
| Per-user | 1000/hour | Per authenticated user | `X-RateLimit-*` |
| Per-IP (unauth) | 100/hour | Per IP address | `X-RateLimit-*` |
| Burst | 50/minute | Per user | Not exposed |

**Rate Limit Exceeded Response**:
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests",
    "retry_after": 3600
  }
}
```
**Status**: `429 Too Many Requests`
**Header**: `Retry-After: 3600`

## Performance Characteristics

| Metric | Typical | P99 | Notes |
|--------|---------|-----|-------|
| Response time | 15ms | 100ms | Without includes |
| Response time | 25ms | 200ms | With `?include=orders` |
| Response size | 500B | 5KB | Depends on includes |

### Optimization Notes

- User lookups are indexed by PK - always fast
- Includes add JOINs; use sparingly for lists
- Response is not cached by default (contains user-specific data)
- Consider adding `ETag` for clients that poll

## Examples

### cURL Examples

```bash
# Get single user (own profile)
curl -X GET "https://api.example.com/api/users/123" \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Accept: application/json"

# Get user with orders included
curl -X GET "https://api.example.com/api/users/123?include=orders" \
  -H "Authorization: Bearer eyJhbG..."

# List users with filtering (admin)
curl -X GET "https://api.example.com/api/users?status=active&page=2&per_page=50" \
  -H "Authorization: Bearer eyJhbG..."

# Create user
curl -X POST "https://api.example.com/api/users" \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Content-Type: application/json" \
  -H "X-Idempotency-Key: unique-request-id-123" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'

# Update user (partial)
curl -X PATCH "https://api.example.com/api/users/123" \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated"}'

# Delete user (soft delete)
curl -X DELETE "https://api.example.com/api/users/123" \
  -H "Authorization: Bearer eyJhbG..."
```

### Python SDK Examples

```python
from myapi import Client

client = Client(token="eyJhbG...")

# Get user
user = client.users.get(123)
print(user.name)

# Get with includes
user = client.users.get(123, include=["orders", "profile"])
print(f"User has {len(user.orders)} orders")

# List with filters
users = client.users.list(
    status="active",
    page=1,
    per_page=50,
    sort="created_at",
    order="desc"
)
for user in users:
    print(user.email)

# Create
new_user = client.users.create(
    name="John Doe",
    email="john@example.com",
    password="securepass123"
)
print(f"Created user {new_user.id}")

# Update
updated = client.users.update(123, name="John Updated")

# Delete
client.users.delete(123)
```

## Related Documentation

- **Entity**: [users](../../data-model/users.md) - Database schema
- **Related Endpoints**:
  - [GET /api/users](./get-api-users.md) - List users
  - [GET /api/users/{id}/orders](./get-api-users-id-orders.md) - User's orders
- **Authentication**: [Auth Guide](../../guides/authentication.md)
- **ETL Usage**: [Step 3: User Sync](../etl/step-03-user-sync.md) - Uses same user data
- **Shared Logic**: `user_repository.py` - Repository pattern shared with ETL
```

---

## Writing Guidelines

1. **Complete Request Spec**: Every parameter, every validation rule, every possible value
2. **Every Error Case**: Not just "returns 400 on error" - list EVERY error code and when it occurs
3. **Security Explicit**: Authentication AND authorization, who can do what
4. **Show The Code**: Include handler code with explanations
5. **SQL Queries**: Show actual queries generated, not just "queries database"
6. **Side Effects**: What else happens besides returning data? Caching, events, webhooks
7. **Real Examples**: Working cURL commands that someone can actually run

## Common Mistakes to Avoid

- DON'T write "validates input" - list EVERY validation rule
- DON'T write "returns error" - specify WHICH error code, WHEN
- DON'T skip auth/authz - who can call this, what can they see
- DON'T forget side effects - cache invalidation, events, etc.
- DON'T use placeholder values - show realistic example data
- DON'T skip the "why" - explain business decisions, not just mechanics
