# Testing Strategies Reference

## Core Philosophy

Tests exist for two reasons only: (1) find bugs in code just written, (2) catch regressions in future changes. Everything else is ritual.

### The 10 Principles

1. **Code first, test smart.** Understand the implementation's tensions and fragile points before writing tests. The implementation reveals WHERE bugs will hide — blind test-first misses this.

2. **Test the API, not the internals.** Always test through the public interface. If you change the implementation, tests should still pass. Internal structure is an implementation detail.

3. **Test states, not lines.** Code coverage measures lines executed, but bugs live in STATE SPACE. A function with 3 branches and 2 parameters has 12+ states — testing 3 fixed inputs covers a fraction.

4. **Informed black-box.** Use knowledge of the implementation to craft inputs that stress boundary conditions, but test through the public API. Know there's a threshold at 256? Test 255, 256, 257 — through the external interface.

5. **Randomize relentlessly.** Fixed test data explores a fixed slice of state space. Random data explores vastly more. Property-based testing with 100 random cases finds bugs that 10 handpicked cases miss.

6. **Bias your randomness.** Pure random data is wasteful — random bytes are all equally uninteresting. Bias random generators toward boundary values, common edge cases, and the specific structures your code handles. For a JSON parser: generate mostly-valid JSON with occasional corruption, not random bytes.

7. **Verify invariants, not outputs.** Instead of checking "output == expected_fixed_value", check "output satisfies invariant." Invariants survive implementation changes. Examples: sorted output is still sorted, round-trip encoding/decoding produces the original, aggregated totals match input totals.

8. **Compare against simplicity.** Write a simple, obviously-correct reference implementation inside the test. Run both on the same random inputs. Differences are bugs in one or the other. The simple version is easy to verify by inspection.

9. **Speed is correctness.** Slow tests don't get run. Tests that don't run don't find bugs. Optimize for fast execution: in-memory over I/O, parallel over sequential, skip unnecessary setup.

10. **LLMs need steering.** "Write tests for X" produces shallow tests with weak assertions. You must explicitly request: boundary stress at specific thresholds, property-based testing with specific invariants, reference implementation comparison, fuzz testing with biased generators.

---

## Strategy Catalog

### 1. Boundary Stress Testing

**When:** Any function with parameters that have thresholds, limits, or type boundaries.

**How:**
1. Read the implementation. Find every comparison (`<`, `>`, `<=`, `>=`, `==`, `!=`), every constant, every limit.
2. For each boundary value N: test N-1, N, N+1.
3. For type boundaries: test at min/max of type (0, -1, MAX_INT, empty string, null).
4. For collection sizes: test empty, one element, boundary size, boundary+1.

**Example boundaries to look for:**
- Buffer sizes, page sizes, batch sizes
- Timeout values, retry counts
- String length limits, array capacity
- Enum ranges, status code categories
- Pagination offsets, limit values

### 2. Property-Based Testing

**When:** Data transformations, serialization/deserialization, pure functions, algorithms.

**Properties to check:**
- **Round-trip:** encode(decode(x)) == x
- **Idempotence:** f(f(x)) == f(x)
- **Monotonicity:** if x < y then f(x) <= f(y)
- **Preservation:** len(transform(list)) == len(list)
- **Commutativity:** f(a, b) == f(b, a) where expected
- **Associativity:** f(f(a, b), c) == f(a, f(b, c))
- **Invariant maintenance:** sum(input) == sum(output) for redistributions

**Libraries:** hypothesis (Python), jqwik (Java), fast-check (TypeScript), swift-testing macros (Swift)

### 3. Invariant / Reference Implementation Testing

**When:** Complex algorithms where a simpler (slower) implementation can serve as oracle.

**How:**
1. Write a naive, obviously-correct implementation inside the test
2. Generate random inputs
3. Run both implementations on same inputs
4. Assert outputs match

**Examples:**
- Optimized sort vs Python's built-in sort
- Custom hash map vs standard library HashMap
- Optimized query builder vs string concatenation
- Compression: decompress(compress(data)) == data AND len(compressed) <= len(data)

### 4. Golden Fixture Regression Testing

**When:** Data pipelines, computation-heavy services, API endpoints with complex responses.

**Architecture:**
1. **Capture phase:** Run code against real data, serialize inputs + outputs as fixtures (Parquet, JSON)
2. **Regression phase:** Load fixtures, re-execute computation, compare outputs against golden baseline
3. **Tolerance:** Use approximate comparison for floating-point, exclude volatile fields (timestamps, IDs)

**Infrastructure patterns:**
- Pytest markers for selective execution (`@pytest.mark.e2e`)
- Root conftest that mocks all external connectors at collection time
- Parametrized fixtures for multiple configurations (plants, environments, tenants)
- Computation caching: run expensive operations once, share across tests
- Checkpoint architecture: capture intermediate states, not just final output

**Comparison utilities needed:**
- `assert_dataframes_equal(actual, expected, tolerance=1e-6, exclude_cols=[...])`
- `normalize_value(val)` — sort lists, handle NaN, canonical JSON for dicts
- `diff_report(actual, expected)` — per-row differences for debugging

### 5. E2E API Lifecycle Testing

**When:** REST/GraphQL endpoints, especially write operations.

**Read endpoints:**
- Capture: call endpoint with representative params, save request + response
- Regression: mock DB/service reads to return captured inputs, assert response matches golden

**Write endpoints — full CRUD lifecycle:**
1. Verify clean state (resource doesn't exist)
2. CREATE — assert 201, verify response schema, verify DB state
3. READ — assert created resource matches
4. UPDATE — assert 200, verify changed fields, verify unchanged fields preserved
5. HISTORY — assert audit trail if applicable
6. DELETE — assert 200/204, verify resource removed
7. Verify clean state restored

**Comparison:**
- Normalize responses: sort lists by natural keys, canonical JSON
- Exclude volatile: timestamps, auto-generated IDs, row numbers
- Status code categories: 2xx = success (including 207 multi-status)
- Float tolerance for computed values

### 6. Live Comparison Testing

**When:** Migrating from legacy to new implementation.

**How:**
1. Start both services (legacy on port A, new on port B)
2. Send identical requests to both
3. Normalize both responses
4. Diff — differences are regressions or intentional changes

**Infrastructure:**
- Script to start both services with correct configs
- Known expected differences documented and excluded
- Report: PASS/FAIL per endpoint with diff details

---

## Anti-Patterns — What NOT to Generate

| Anti-pattern | Why it's bad | What to do instead |
|---|---|---|
| `assertNotNull(result)` as sole assertion | Proves function returns something, not that it's correct | Assert specific value, shape, or invariant |
| `assertEquals(result, result)` | Tautology — always passes | Assert against independently computed expected value |
| Test with no assertions | Tests that code doesn't crash, nothing else | Add invariant or property assertions |
| Hardcoded input/output pairs only | Tests one state, misses boundary cases | Add property-based tests alongside specific cases |
| Mocking everything | Tests the mocks, not the code | Mock only external boundaries (DB, HTTP, filesystem) |
| Testing private methods | Couples tests to implementation | Test through public API |
| One test per method (happy path) | Misses error paths, boundaries, state interactions | Multiple tests per method: happy, error, boundary, property |
| `try/catch` that swallows assertion errors | Test always passes | Let assertions propagate |
| Tests that depend on execution order | Fragile, non-reproducible | Each test sets up its own state |
| Slow tests without `@pytest.mark.slow` / tag | Block fast feedback loop | Mark slow tests, run separately |
