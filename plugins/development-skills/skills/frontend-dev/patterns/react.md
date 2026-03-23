# React Patterns & Standards

Shared React patterns for all React-based projects (standalone, Vite, Raycast, Next.js). Referenced by the frontend-dev skill during Research and Implementation phases.

---

## Review Standards

Enforce these during Staff Engineer Review (Phase 6):

- Hooks follow Rules of Hooks (no conditional hooks, no hooks in loops)
- Components decomposed (< 70 lines each, single responsibility)
- State management appropriate — local state for UI, context/stores for shared state
- No premature memoization (`useMemo`/`useCallback` only when profiling shows need)
- Props typed with TypeScript — inline for simple, separate type for complex/reusable
- Event handlers named with `handle` prefix (`handleClick`, `handleSubmit`)
- Custom hooks extract reusable logic — named with `use` prefix
- No `any` types
- No direct DOM manipulation — use refs when necessary

---

## Component Patterns

### Props Typing

```tsx
// Inline type for simple components
function Button({ label, onClick }: { label: string; onClick: () => void }) {
  return <button onClick={onClick}>{label}</button>;
}

// Separate type for complex/reusable components
type CardProps = {
  title: string;
  children: React.ReactNode;
  variant?: "default" | "outlined";
};

function Card({ title, children, variant = "default" }: CardProps) {
  return <div className={variant}><h2>{title}</h2>{children}</div>;
}

// Extend HTML element props
type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "primary" | "secondary";
};

function Button({ variant = "primary", ...props }: ButtonProps) {
  return <button className={variant} {...props} />;
}
```

---

## Hooks Patterns

### Custom Hooks

```tsx
// Extract reusable logic into custom hooks
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// Async data hook
function useFetch<T>(url: string) {
  const [state, setState] = useState<AsyncState<T>>({ status: "idle" });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });

    fetch(url)
      .then(res => res.json())
      .then(data => { if (!cancelled) setState({ status: "success", data }); })
      .catch(error => { if (!cancelled) setState({ status: "error", error }); });

    return () => { cancelled = true; };
  }, [url]);

  return state;
}
```

### Rules of Hooks

```tsx
// GOOD: Hooks at top level, always called
function Component({ showDetails }: { showDetails: boolean }) {
  const [count, setCount] = useState(0);
  const data = useFetch("/api/data");

  if (!showDetails) return null;
  return <div>{count} - {JSON.stringify(data)}</div>;
}

// BAD: Conditional hook
function Component({ showDetails }: { showDetails: boolean }) {
  if (showDetails) {
    const [count, setCount] = useState(0); // VIOLATION
  }
}
```

---

## State Management

### When to Use What

```
Local state (useState):        UI state — modals, tabs, form inputs
Derived state (useMemo):       Computed from existing state/props
Context (createContext):        Theme, auth, locale — read by many, updated rarely
External store (Zustand/Redux): Complex shared state, frequent updates, DevTools needed
URL state (searchParams):       Filters, pagination, shareable state
```

### React Context

```tsx
"use client"; // Only needed in Next.js

import { createContext, useContext, useState, ReactNode } from "react";

type Theme = "light" | "dark";

const ThemeContext = createContext<{
  theme: Theme;
  toggle: () => void;
} | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light");
  const toggle = () => setTheme(t => (t === "light" ? "dark" : "light"));

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be used within ThemeProvider");
  return context;
}
```

---

## Styling

Consistent approach within project. Common options:

| Approach | Pros | Cons |
|----------|------|------|
| CSS Modules | Scoped, no runtime | Verbose class names |
| Tailwind CSS | Rapid development | Learning curve, verbose markup |
| CSS-in-JS | Dynamic styles | Runtime overhead, SSR complexity |

**Principles:**
- Be consistent within the project
- Avoid inline styles in production code
- Co-locate styles with components when possible

---

## Testing

### Component Tests with @testing-library/react

```tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("renders with label", () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  it("calls onClick when clicked", () => {
    const handleClick = vi.fn();
    render(<Button label="Click" onClick={handleClick} />);
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Testing Hooks

```tsx
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("increments count", () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });
});
```

---

## Quick Reference

| Need | Do This |
|------|---------|
| Type component props | Inline type or separate type |
| Extend HTML props | `React.ComponentProps<"element">` |
| Reusable logic | Custom hook with `use` prefix |
| Share state across tree | React Context or external store |
| URL-based state | URLSearchParams |
| Test component | @testing-library/react with `render`, `screen` |
| Test hook | `renderHook` from @testing-library/react |

## What NOT to Do

| Anti-Pattern | Instead |
|--------------|---------|
| Inline styles | CSS Modules, Tailwind, or CSS-in-JS |
| Giant components (> 70 lines) | Split into smaller, focused components |
| Barrel exports for everything | Direct imports, barrel only for public API |
| `useEffect` for derived state | `useMemo` or compute inline |
| Premature `useMemo`/`useCallback` | Profile first, optimize when measured |
| Prop drilling through 3+ levels | Context or composition pattern |

See also: [typescript.md](typescript.md) for TypeScript-specific anti-patterns (`any`, `@ts-ignore`, etc.)
