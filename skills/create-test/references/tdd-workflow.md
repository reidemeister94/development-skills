# TDD Workflow — Red/Green/Refactor

Test-driven development with the red-green-refactor loop. Use when the task requires building a feature or fixing a bug **test-first**, or when the user mentions "TDD", "red-green-refactor", "test-first development".

**When to apply**: new features with clear behavior, reproducible bug fixes, refactors with coverage tests. **When NOT**: exploratory prototypes where behavior emerges only as you write code.

## Philosophy

**Core principle**: tests should verify *behavior* through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests**: integration-style. They exercise real code paths through public APIs. They describe *what* the system does, not *how*. A good test reads like a specification — `"user can checkout with valid cart"` tells you exactly what capability exists. They survive refactors.

**Bad tests**: coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (e.g. direct DB query instead of the interface). Warning sign: the test breaks when you refactor without behavior change.

See "Good vs Bad Tests" and "Mocking" sections below.

## Anti-pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code".

It produces **crap tests**:

- Tests written in bulk verify *imagined* behavior, not *actual* behavior.
- You end up testing the *shape* of things (data structures, signatures) instead of user-visible behavior.
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine.
- You outrun your headlights, committing to test structure before understanding the implementation.

**Correct approach**: vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly which behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

## Workflow

### 1. Planning

Before writing any code:

- Confirm with the user which interface changes are needed.
- Confirm which behaviors to test (prioritize).
- Identify opportunities for **deep modules** (small interface, deep implementation) — see `roast-my-code/references/architectural-depth.md`.
- List the behaviors to test (not the implementation steps).
- Get user approval on the plan.

Ask the user: "What should the public interface look like? Which behaviors matter most?"

**You can't test everything.** Confirm exactly which behaviors matter. Concentrate test effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → fails
GREEN: Write minimal code to pass → passes
```

This is your tracer bullet — proves the path works end-to-end.

### 3. Incremental loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time.
- Only enough code to pass the current test.
- Don't anticipate future tests.
- Keep tests focused on observable behavior.

### 4. Refactor

When all tests pass, look for refactor candidates:

- Extract duplication.
- Deepen modules (move complexity behind simple interfaces — see `architectural-depth.md`).
- Apply SOLID principles where natural.
- Consider what new code reveals about existing code.
- Run tests after each refactor step.

**Never refactor while RED.** Get to GREEN first.

## Per-cycle checklist

```
[ ] The test describes behavior, not implementation
[ ] The test uses the public interface only
[ ] The test would survive an internal refactor
[ ] The code is minimal for this test
[ ] No speculative features added
```

## Good vs Bad Tests

### Good test (integration-style)

```python
# GOOD: tests observable behavior through the public interface
def test_user_can_checkout_with_valid_cart():
    cart = create_cart()
    cart.add(product)
    result = checkout(cart, payment_method)
    assert result.status == "confirmed"
```

Characteristics:

- Tests behavior callers/users care about.
- Uses public API only.
- Survives internal refactors.
- Describes **WHAT**, not **HOW**.
- One logical assertion per test.

### Bad test (implementation-coupled)

```python
# BAD: tests implementation details
def test_checkout_calls_payment_service_process():
    mock_payment = mocker.patch('payment_service.process')
    checkout(cart, payment)
    mock_payment.assert_called_once_with(cart.total)
```

Red flags:

- Mocking internal collaborators.
- Testing private methods.
- Asserting on call counts/order.
- Test breaks on refactor without behavior change.
- Test name describes HOW, not WHAT.
- Verifying through external channels instead of the interface.

```python
# BAD: bypasses the interface to verify
def test_create_user_saves_to_database():
    create_user(name="Alice")
    row = db.query("SELECT * FROM users WHERE name = 'Alice'").first()
    assert row is not None

# GOOD: verifies through the interface
def test_create_user_makes_user_retrievable():
    user = create_user(name="Alice")
    retrieved = get_user(user.id)
    assert retrieved.name == "Alice"
```

## Mocking — only at boundaries

Mock ONLY at **system boundaries**:

- External APIs (payment, email, SMS).
- Databases (sometimes — prefer a real test DB).
- Time / randomness.
- File system (sometimes).

**Don't mock**:

- Your own classes/modules.
- Internal collaborators.
- Anything you control.

### Designing for mockability

At boundaries, design interfaces that are easy to mock:

**1. Dependency injection**

Pass external dependencies in rather than creating them internally:

```python
# Easy to mock
def process_payment(order, payment_client):
    return payment_client.charge(order.total)

# Hard to mock
def process_payment(order):
    client = StripeClient(os.environ["STRIPE_KEY"])
    return client.charge(order.total)
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```python
# GOOD: each function is independently mockable
class Api:
    def get_user(self, id): ...
    def get_orders(self, user_id): ...
    def create_order(self, data): ...

# BAD: mocking requires conditional logic inside the mock
class Api:
    def fetch(self, endpoint, options): ...
```

The SDK approach means:

- Each mock returns one specific shape.
- No conditional logic in test setup.
- Easier to see which endpoints a test exercises.
- Type safety per endpoint.

## Cross-link

- Deep modules / deletion test / architecture glossary: `roast-my-code/references/architectural-depth.md`.
- Advanced test patterns (property-based, characterization, golden fixture, e2e): other files in `create-test/references/`.
