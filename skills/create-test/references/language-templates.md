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
