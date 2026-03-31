# Language Templates Reference

## Python (pytest + hypothesis)

### Test file scaffold

```python
"""Tests for {module_name} — boundary, property, and invariant testing."""
import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from {module_path} import {functions_under_test}


# --- Boundary Tests ---

class TestBoundary{FunctionName}:
    """Boundary stress tests at identified thresholds."""

    @pytest.mark.parametrize("input_val, expected", [
        (THRESHOLD - 1, ...),  # Just below boundary
        (THRESHOLD, ...),      # At boundary
        (THRESHOLD + 1, ...),  # Just above boundary
    ])
    def test_{function}_at_boundary(self, input_val, expected):
        result = {function}(input_val)
        assert result == expected

    def test_{function}_empty_input(self):
        result = {function}(EMPTY)
        assert result == EXPECTED_FOR_EMPTY

    def test_{function}_null_handling(self):
        with pytest.raises(EXPECTED_ERROR):
            {function}(None)


# --- Property-Based Tests ---

class TestProperties{FunctionName}:
    """Invariants verified over random inputs."""

    @given(st.{strategy}())
    @settings(max_examples=200)
    def test_{invariant_name}(self, data):
        result = {function}(data)
        assert INVARIANT_HOLDS(result, data)

    @given(st.{strategy}())
    def test_round_trip(self, data):
        encoded = encode(data)
        decoded = decode(encoded)
        assert decoded == data


# --- Reference Implementation Tests ---

class TestInvariant{FunctionName}:
    """Compare optimized implementation against simple reference."""

    @given(st.lists(st.integers(), min_size=0, max_size=1000))
    def test_matches_reference(self, data):
        def reference_impl(d):
            # Simple, obviously correct version
            return sorted(d)

        assert {function}(data) == reference_impl(data)


# --- Random Stress Tests ---

class TestStress{FunctionName}:
    """High-volume random testing for edge cases."""

    @given(st.{strategy}())
    @settings(max_examples=1000)
    def test_no_crash_on_random_input(self, data):
        result = {function}(data)
        assert result is not None
        # Plus specific invariant assertions:
        assert INVARIANT(result)
```

### Hypothesis strategies for common types

```python
# Strings biased toward boundaries
st.text(min_size=0, max_size=300).filter(lambda s: len(s) in range(LIMIT-2, LIMIT+3))

# Integers near boundaries
st.integers(min_value=THRESHOLD-10, max_value=THRESHOLD+10)

# DataFrames (with pandas)
@st.composite
def dataframes(draw):
    n_rows = draw(st.integers(min_value=0, max_value=100))
    return pd.DataFrame({
        "col_a": draw(st.lists(st.integers(), min_size=n_rows, max_size=n_rows)),
        "col_b": draw(st.lists(st.text(min_size=1), min_size=n_rows, max_size=n_rows)),
    })

# JSON-like structures (for parser testing)
json_values = st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text(),
    lambda children: st.lists(children) | st.dictionaries(st.text(min_size=1), children),
    max_leaves=50,
)
```

### Hypothesis composite strategies for domain objects

```python
from hypothesis import strategies as st

@st.composite
def valid_orders(draw):
    """Generate realistic Order objects with valid relationships."""
    user_id = draw(st.integers(min_value=1))
    items = draw(st.lists(
        st.builds(OrderItem,
            product_id=st.integers(min_value=1),
            quantity=st.integers(min_value=1, max_value=100),
            price=st.decimals(min_value=Decimal("0.01"), max_value=Decimal("9999.99")),
        ),
        min_size=1, max_size=20,
    ))
    return Order(user_id=user_id, items=items)

@st.composite
def valid_date_ranges(draw):
    """Generate start/end date pairs where start < end."""
    start = draw(st.dates())
    delta = draw(st.timedeltas(min_value=timedelta(days=1), max_value=timedelta(days=365)))
    return start, start + delta

# Use in tests:
@given(order=valid_orders())
def test_order_total_matches_items(order):
    assert order.total == sum(item.price * item.quantity for item in order.items)
```

### Hypothesis settings profiles

```python
# conftest.py — configure profiles for different environments
from hypothesis import settings, Phase, HealthCheck

settings.register_profile("ci", max_examples=1000, deadline=None,
    suppress_health_check=[HealthCheck.too_slow])
settings.register_profile("dev", max_examples=50, deadline=500)
settings.register_profile("debug", max_examples=10,
    phases=[Phase.explicit, Phase.generate])

# Activate via CLI: pytest --hypothesis-profile=ci
# Or in pyproject.toml:
# [tool.hypothesis]
# default = "dev"
```

### Mutation testing setup (mutmut)

```bash
# Install
pip install mutmut

# Run against specific module
mutmut run --paths-to-mutate=src/core/

# View surviving mutants (tests didn't catch these bugs)
mutmut results
mutmut show <id>  # inspect a specific surviving mutant

# CI integration: fail if mutation score drops below threshold
mutmut run --paths-to-mutate=src/core/ && mutmut results --json | \
  python -c "import sys,json; d=json.load(sys.stdin); \
  sys.exit(0 if d['killed']/(d['killed']+d['survived']) > 0.85 else 1)"
```

### Contract testing scaffold (Pact — Python consumer)

```python
"""Consumer-driven contract test — defines what this service expects from provider."""
import pytest
from pathlib import Path
from pact.v3 import Pact, match

@pytest.fixture
def pact():
    pact = Pact("my-consumer", "user-provider").with_specification("V4")
    yield pact
    pact.write_file(Path(__file__).parent / "pacts")

def test_get_user(pact):
    expected_response = {
        "id": match.int(123),
        "name": match.str("Alice"),
        "email": match.regex(r".+@.+\..+", "alice@example.com"),
    }
    (
        pact.upon_receiving("A user request")
        .given("the user exists", parameters={"id": 123})
        .with_request("GET", "/users/123")
        .will_respond_with(200)
        .with_body(expected_response, content_type="application/json")
    )
    with pact.serve() as srv:
        # Call your actual client code against the mock server
        client = UserClient(str(srv.url))
        user = client.get_user(123)
        assert user.name == "Alice"
```

### Golden fixture patterns (pytest)

```python
# conftest.py — golden fixture loading
import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "golden"

@pytest.fixture(params=["config_a", "config_b"])
def config_name(request) -> str:
    return request.param

@pytest.fixture
def golden_data(config_name: str) -> dict:
    fixture_dir = FIXTURES_DIR / config_name
    return {
        "inputs": {f.stem: json.loads(f.read_text()) for f in (fixture_dir / "inputs").glob("*.json")},
        "outputs": {f.stem: json.loads(f.read_text()) for f in (fixture_dir / "outputs").glob("*.json")},
    }

# Capture script
def capture_golden(config_name: str):
    """Run once against live system to capture golden fixtures."""
    inputs = fetch_real_inputs(config_name)
    outputs = compute(inputs)
    fixture_dir = FIXTURES_DIR / config_name
    (fixture_dir / "inputs").mkdir(parents=True, exist_ok=True)
    (fixture_dir / "outputs").mkdir(parents=True, exist_ok=True)
    for name, data in inputs.items():
        (fixture_dir / "inputs" / f"{name}.json").write_text(json.dumps(data, default=str, indent=2))
    for name, data in outputs.items():
        (fixture_dir / "outputs" / f"{name}.json").write_text(json.dumps(data, default=str, indent=2))
```

### Integration test scaffold (pytest + testcontainers)

```python
"""Integration tests for {module_name} — real PostgreSQL, transaction-isolated."""
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from {module_path} import {repository_or_service}


# --- Container Fixtures (conftest.py, session scope) ---

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg

@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


# --- Factory Fixtures ---

@pytest.fixture
def make_{entity}(db_session):
    def make(field_a="default_a", field_b=42, **overrides):
        obj = {Entity}(field_a=field_a, field_b=field_b, **overrides)
        db_session.add(obj)
        db_session.flush()
        return obj
    yield make


# --- Integration Tests ---

class TestRepository{Entity}:
    """Tests against real PostgreSQL — each test rolls back."""

    def test_create_and_retrieve(self, db_session, make_{entity}):
        entity = make_{entity}(field_a="test_value")
        result = {repository}.get_by_id(db_session, entity.id)
        assert result is not None
        assert result.field_a == "test_value"

    def test_unique_constraint_enforced(self, db_session, make_{entity}):
        make_{entity}(unique_field="taken")
        with pytest.raises(IntegrityError):
            make_{entity}(unique_field="taken")

    def test_query_filters_correctly(self, db_session, make_{entity}):
        make_{entity}(status="active")
        make_{entity}(status="active")
        make_{entity}(status="inactive")
        results = {repository}.find_by_status(db_session, "active")
        assert len(results) == 2
        assert all(r.status == "active" for r in results)

    def test_aggregation_accuracy(self, db_session, make_{entity}):
        make_{entity}(amount=100.0)
        make_{entity}(amount=250.5)
        make_{entity}(amount=49.5)
        total = {repository}.sum_amounts(db_session)
        assert total == pytest.approx(400.0)
```

### Concurrency test scaffold (pytest + asyncio)

```python
"""Concurrency tests for {module_name} — race conditions, atomicity."""
import asyncio
import pytest

from {module_path} import {async_function}


@pytest.mark.asyncio
class TestConcurrency{Feature}:
    """Verify correctness under concurrent access."""

    async def test_no_double_booking(self, db_session, make_resource):
        """Two concurrent claims on last resource — exactly one wins."""
        resource = make_resource(available=1)
        results = await asyncio.gather(
            {async_function}(resource.id, user_a),
            {async_function}(resource.id, user_b),
            return_exceptions=True,
        )
        successes = [r for r in results if not isinstance(r, Exception)]
        assert len(successes) == 1

    async def test_counter_atomicity(self, db_session, make_counter):
        """N concurrent increments produce exactly +N."""
        counter = make_counter(value=0)
        N = 50
        await asyncio.gather(*[
            increment_counter(counter.id) for _ in range(N)
        ])
        refreshed = await get_counter(counter.id)
        assert refreshed.value == N

    async def test_idempotent_operation(self, db_session, make_resource):
        """Duplicate requests with same key produce same result."""
        key = "idempotency-key-123"
        r1 = await {async_function}(key=key, amount=100)
        r2 = await {async_function}(key=key, amount=100)
        assert r1.id == r2.id  # same record, not duplicated
```

### Characterization test scaffold (approval testing)

```python
"""Characterization tests for {module_name} — locks current behavior for safe refactoring."""
import json
import pytest
from pathlib import Path

from {module_path} import {function_under_test}

BASELINES_DIR = Path(__file__).parent / "baselines"


def normalize(obj):
    """Scrub volatile fields for deterministic comparison."""
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in sorted(obj.items())
                if k not in ("timestamp", "updated_at", "request_id")}
    if isinstance(obj, list):
        return [normalize(item) for item in obj]
    if isinstance(obj, float):
        return round(obj, 6)
    return obj


class TestCharacterization{Module}:
    """WARNING: These tests lock CURRENT behavior, including bugs.
    Failures after refactoring = behavior changed (intended or not)."""

    @pytest.mark.parametrize("case_name", ["case_a", "case_b", "case_c"])
    def test_output_matches_baseline(self, case_name):
        input_file = BASELINES_DIR / case_name / "input.json"
        baseline_file = BASELINES_DIR / case_name / "output.json"

        input_data = json.loads(input_file.read_text())
        actual = {function_under_test}(**input_data)
        actual_normalized = normalize(actual)

        if not baseline_file.exists():
            # First run: capture baseline
            baseline_file.parent.mkdir(parents=True, exist_ok=True)
            baseline_file.write_text(json.dumps(actual_normalized, indent=2))
            pytest.skip(f"Baseline captured for {case_name} — re-run to verify")

        expected = json.loads(baseline_file.read_text())
        assert actual_normalized == expected, (
            f"Behavior changed for {case_name}. "
            f"If intentional, delete {baseline_file} and re-run to capture new baseline."
        )


# --- Capture Script (run once to generate baselines) ---

def capture_baselines():
    """Run against live system to capture golden baselines.
    Usage: python -c 'from test_{module} import capture_baselines; capture_baselines()'
    """
    cases = {
        "case_a": {"param1": "value1", "param2": 42},
        "case_b": {"param1": "value2", "param2": 0},
        "case_c": {"param1": "edge_case", "param2": -1},
    }
    for name, inputs in cases.items():
        output = {function_under_test}(**inputs)
        case_dir = BASELINES_DIR / name
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "input.json").write_text(json.dumps(inputs, indent=2))
        (case_dir / "output.json").write_text(json.dumps(normalize(output), indent=2))
    print(f"Captured {len(cases)} baselines to {BASELINES_DIR}")
```

---

## Java (JUnit 5 + jqwik)

### Test file scaffold

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import net.jqwik.api.*;
import static org.assertj.core.api.Assertions.*;

class {ClassName}Test {

    // --- Boundary Tests ---

    @ParameterizedTest
    @CsvSource({
        "255, EXPECTED_BELOW",    // Below boundary
        "256, EXPECTED_AT",       // At boundary
        "257, EXPECTED_ABOVE",    // Above boundary
    })
    void boundaryTest(int input, String expected) {
        var result = subject.method(input);
        assertThat(result).isEqualTo(expected);
    }

    @Test
    void emptyInputReturnsDefault() {
        var result = subject.method(List.of());
        assertThat(result).isEmpty();
    }

    @Test
    void nullInputThrows() {
        assertThatThrownBy(() -> subject.method(null))
            .isInstanceOf(IllegalArgumentException.class);
    }

    // --- Property-Based Tests (jqwik) ---

    @Property(tries = 200)
    void roundTrip(@ForAll String input) {
        var encoded = subject.encode(input);
        var decoded = subject.decode(encoded);
        assertThat(decoded).isEqualTo(input);
    }

    @Property
    void outputAlwaysSorted(@ForAll List<@IntRange(min = -1000, max = 1000) Integer> input) {
        var result = subject.sort(input);
        assertThat(result).isSorted();
        assertThat(result).hasSameSizeAs(input);
    }

    // --- Reference Implementation ---

    @Property(tries = 500)
    void matchesReference(@ForAll @Size(max = 100) List<Integer> data) {
        var optimized = subject.process(data);
        var reference = referenceImpl(data);
        assertThat(optimized).isEqualTo(reference);
    }

    private List<Integer> referenceImpl(List<Integer> data) {
        // Simple, obviously correct version
        return data.stream().sorted().toList();
    }
}
```

---

## TypeScript (vitest + fast-check)

### Test file scaffold

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { functionUnderTest } from '../src/module';

describe('functionUnderTest', () => {

  // --- Boundary Tests ---

  it.each([
    [THRESHOLD - 1, EXPECTED_BELOW],
    [THRESHOLD, EXPECTED_AT],
    [THRESHOLD + 1, EXPECTED_ABOVE],
  ])('handles boundary value %i', (input, expected) => {
    expect(functionUnderTest(input)).toEqual(expected);
  });

  it('handles empty input', () => {
    expect(functionUnderTest([])).toEqual([]);
  });

  it('throws on null input', () => {
    expect(() => functionUnderTest(null as any)).toThrow();
  });

  // --- Property-Based Tests ---

  it('round-trip encoding', () => {
    fc.assert(
      fc.property(fc.string(), (input) => {
        const encoded = encode(input);
        const decoded = decode(encoded);
        expect(decoded).toEqual(input);
      }),
      { numRuns: 200 },
    );
  });

  it('output preserves invariant', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (data) => {
        const result = functionUnderTest(data);
        // Invariant: output length matches input
        expect(result).toHaveLength(data.length);
        // Invariant: output is sorted
        for (let i = 1; i < result.length; i++) {
          expect(result[i]).toBeGreaterThanOrEqual(result[i - 1]);
        }
      }),
    );
  });

  // --- Reference Implementation ---

  it('matches naive implementation', () => {
    fc.assert(
      fc.property(fc.array(fc.integer(), { maxLength: 100 }), (data) => {
        const optimized = functionUnderTest(data);
        const reference = [...data].sort((a, b) => a - b); // naive
        expect(optimized).toEqual(reference);
      }),
      { numRuns: 500 },
    );
  });
});
```

### API endpoint test (golden fixture)

```typescript
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync } from 'fs';
import { join } from 'path';

const FIXTURES_DIR = join(__dirname, 'fixtures', 'golden');

describe('GET /api/resource', () => {
  let goldenResponse: any;

  beforeAll(() => {
    goldenResponse = JSON.parse(
      readFileSync(join(FIXTURES_DIR, 'resource-list.json'), 'utf-8')
    );
  });

  it('matches golden fixture', async () => {
    const response = await app.request('/api/resource');
    const body = await response.json();
    const normalized = normalize(body);
    expect(normalized).toEqual(normalize(goldenResponse));
  });
});

function normalize(obj: unknown): unknown {
  if (Array.isArray(obj)) return obj.map(normalize).sort(byNaturalKey);
  if (obj && typeof obj === 'object') {
    const { timestamp, updatedAt, ...rest } = obj as Record<string, unknown>;
    return Object.fromEntries(
      Object.entries(rest).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => [k, normalize(v)])
    );
  }
  return obj;
}
```

### Playwright E2E scaffold

```typescript
import { test, expect, type Page, type Locator } from '@playwright/test';

// --- Page Object ---

class {PageName}Page {
  constructor(private readonly page: Page) {}

  get url() { return '/{route}'; }

  // Lazy getters — resolved when accessed, never stale
  get heading(): Locator {
    return this.page.getByRole('heading', { level: 1 });
  }

  get submitButton(): Locator {
    return this.page.getByRole('button', { name: '{ActionLabel}' });
  }

  get inputField(): Locator {
    return this.page.getByLabel('{FieldLabel}');
  }

  get errorMessage(): Locator {
    return this.page.getByRole('alert');
  }

  async goto(): Promise<void> {
    await this.page.goto(this.url);
  }

  async fillAndSubmit(value: string): Promise<void> {
    await this.inputField.fill(value);
    await this.submitButton.click();
  }
}


// --- Custom Fixture ---

const pageTest = test.extend<{ {pageName}Page: {PageName}Page }>({
  {pageName}Page: async ({ page }, use) => {
    await use(new {PageName}Page(page));
  },
});


// --- E2E Tests ---

pageTest.describe('{Feature} flows', () => {

  pageTest('happy path: complete {action}', async ({ {pageName}Page }) => {
    await {pageName}Page.goto();
    await expect({pageName}Page.heading).toBeVisible();

    await {pageName}Page.fillAndSubmit('valid input');

    // Web-first assertion — auto-retries until timeout
    await expect({pageName}Page.page).toHaveURL(/\/success/);
  });

  pageTest('validation: shows error on invalid input', async ({ {pageName}Page }) => {
    await {pageName}Page.goto();
    await {pageName}Page.fillAndSubmit('');

    await expect({pageName}Page.errorMessage).toContainText('required');
  });

  pageTest('handles API error gracefully', async ({ {pageName}Page }) => {
    // Mock API failure
    await {pageName}Page.page.route('**/api/{endpoint}', (route) =>
      route.fulfill({ status: 500, body: '{"error": "Server Error"}' })
    );

    await {pageName}Page.goto();
    await {pageName}Page.fillAndSubmit('valid input');

    await expect({pageName}Page.errorMessage).toContainText('try again');
  });
});


// --- Visual Regression ---

pageTest.describe('@visual {Feature} snapshots', () => {

  pageTest('default state renders correctly', async ({ {pageName}Page }) => {
    await {pageName}Page.goto();
    await expect({pageName}Page.page.locator('main')).toHaveScreenshot(
      '{feature}-default.png',
      {
        animations: 'disabled',
        mask: [{pageName}Page.page.locator('[data-testid="timestamp"]')],
      }
    );
  });
});
```

### Contract testing scaffold (Pact — TypeScript consumer)

```typescript
import { PactV4, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV4({
  consumer: 'my-frontend',
  provider: 'user-api',
});

describe('User API Contract', () => {
  it('fetches a user by ID', async () => {
    await provider
      .addInteraction()
      .given('user 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest('GET', '/users/123')
      .willRespondWith(200, (builder) => {
        builder.jsonBody({
          id: MatchersV3.integer(123),
          name: MatchersV3.string('Alice'),
          email: MatchersV3.regex(/.*@.*\..*/, 'alice@example.com'),
        });
      })
      .executeTest(async (mockserver) => {
        const client = new UserClient(mockserver.url);
        const user = await client.getUser(123);
        expect(user.name).toBe('Alice');
      });
  });
});
```

### Mutation testing setup (Stryker — TypeScript)

```bash
# Install
npm install --save-dev @stryker-mutator/core @stryker-mutator/vitest-runner

# Init config
npx stryker init

# Run
npx stryker run

# CI: check threshold in stryker.config.mjs
# thresholds: { high: 90, low: 80, break: 75 }
```

---

## Swift (XCTest + swift-testing)

### Test file scaffold

```swift
import Testing
@testable import ModuleName

struct FunctionNameTests {

    // --- Boundary Tests ---

    @Test("Handles value at boundary", arguments: [
        (THRESHOLD - 1, ExpectedBelow),
        (THRESHOLD, ExpectedAt),
        (THRESHOLD + 1, ExpectedAbove),
    ])
    func boundary(input: Int, expected: Output) {
        let result = functionUnderTest(input)
        #expect(result == expected)
    }

    @Test("Handles empty input")
    func emptyInput() {
        let result = functionUnderTest([])
        #expect(result.isEmpty)
    }

    // --- Invariant Tests ---

    @Test("Round-trip encode/decode preserves data")
    func roundTrip() {
        for _ in 0..<200 {
            let input = randomInput()
            let encoded = encode(input)
            let decoded = decode(encoded)
            #expect(decoded == input)
        }
    }

    @Test("Output matches reference implementation")
    func matchesReference() {
        for _ in 0..<500 {
            let data = (0..<Int.random(in: 0...100)).map { _ in Int.random(in: -1000...1000) }
            let optimized = functionUnderTest(data)
            let reference = data.sorted() // naive
            #expect(optimized == reference)
        }
    }

    private func randomInput() -> String {
        let length = Int.random(in: 0...300)
        return String((0..<length).map { _ in Character(UnicodeScalar(Int.random(in: 32...126))!) })
    }
}
```
