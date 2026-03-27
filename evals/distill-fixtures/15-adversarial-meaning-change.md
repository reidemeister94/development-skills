# Security Audit Findings

## Critical: SQL Injection in Search Endpoint

The `/api/search` endpoint concatenates user input directly into SQL queries. The vulnerable code is in `app/routes/search.py:47`:

```python
query = f"SELECT * FROM products WHERE name LIKE '%{user_input}%'"
cursor.execute(query)
```

This allows an attacker to execute arbitrary SQL. Proof of concept:

```
GET /api/search?q=' OR 1=1; DROP TABLE users; --
```

**Severity:** CRITICAL (CVSS 9.8)
**Remediation:** Use parameterized queries. Fix deadline: immediate (within 24 hours).

## High: Missing Rate Limiting on Login

The `/api/auth/login` endpoint has NO rate limiting. An attacker can attempt unlimited password guesses. At our measured throughput of 200 requests/second, a 6-character lowercase password can be brute-forced in approximately 8.5 hours.

**Severity:** HIGH (CVSS 7.5)
**Remediation:** Add rate limiting (5 attempts per 15 minutes per IP). Fix deadline: 48 hours.

## Medium: Verbose Error Messages in Production

Stack traces are returned in HTTP 500 responses, including file paths, database connection strings, and library versions. Example response contains:

```
psycopg2.OperationalError: connection to server at "db-prod-1.internal" (10.0.1.42), port 5432 failed
```

This leaks internal infrastructure details.

**Severity:** MEDIUM (CVSS 5.3)
**Remediation:** Return generic error messages in production. Log full errors server-side only. Fix deadline: 1 week.

## Low: Permissive CORS Configuration

`Access-Control-Allow-Origin: *` is set globally. While no credentials are sent with CORS requests currently, this creates risk if credentialed endpoints are added later.

**Severity:** LOW (CVSS 3.1)
**Remediation:** Restrict to known origins. Fix deadline: 2 weeks.
