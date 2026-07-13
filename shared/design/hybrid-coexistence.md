# MUI and shadcn coexistence

Use only when both libraries are present. Project rules override this default.

## Component ownership

Keep MUI for DataGrid Pro, TextField, Autocomplete, and date/range pickers. Prefer shadcn for shells and simple controls: dialog, menu, popover, tooltip, tabs, card, badge, button, checkbox, switch, slider, alert, skeleton, sidebar, sheet, and simple select. Migration is explicit work, never a side effect of editing an existing component.

## CSS and DataGrid

Declare this before Tailwind imports so utilities and MUI resolve predictably:

```css
@layer theme, base, mui, components, utilities;
```

Next.js must wrap the app with `AppRouterCacheProvider` so MUI uses its layer. Tailwind preflight also needs one global DataGrid escape hatch:

```css
.MuiInputBase-input { box-sizing: content-box; }
```

## Dialog focus

For a shadcn dialog containing MUI without portal panels, prevent initial focus steal:

```tsx
<DialogContent onOpenAutoFocus={(event) => event.preventDefault()}>
```

When DataGrid panels, Autocomplete, or other MUI portals must work, use a project backdrop and a non-modal Radix dialog. Use that form only when a portal requires it. Render a child dialog as a sibling, never nested inside its parent.

## Visual consistency

Use one input family within a form or filter bar. Use Lucide for shadcn and general UI; use MUI icons inside MUI controls. Never mix icon libraries within one component.

MUI consumes `theme.*`; shadcn and Tailwind consume the project's CSS variables. Do not pass one token vocabulary into the other component family.
