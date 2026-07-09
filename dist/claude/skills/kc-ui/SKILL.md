---
name: kc-ui
description: Select and apply curated UI style presets for web, desktop, and mobile interfaces. Use when the user types /kc-ui, $kc-ui, kc-ui, asks to list available UI styles, inspect one UI style, or apply an explicitly named UI style to a page, component, or project UI.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# UI Style

## Description

List, inspect, and apply curated UI style presets to the current project. This skill is a style library and execution workflow for web, desktop, and mobile interfaces, not a single fixed template.

## Parameters

- Required for applying UI changes: an explicit built-in style id and a UI task.
- Optional for listing: no parameters.
- Optional for inspection: one built-in style id.
- Current built-in style id: `agency-compact`.
- If the user asks for a generic style such as dark, minimal, Apple-like, compact, or native without naming a style id, do not edit code. List available style ids with one-line descriptions and ask the user to rerun with an explicit style id.
- If the style id is unknown, do not edit code. List available style ids and show the expected command shape.

## Shortcuts And Commands

- Codex list command: `$kc-ui list`
- Codex inspect command: `$kc-ui look <style-id>`
- Codex apply command: `$kc-ui use <style-id> <task>`
- Codex shorthand apply command: `$kc-ui <style-id> <task>`
- Claude Code list command: `/kc-ui list`
- Claude Code inspect command: `/kc-ui look <style-id>`
- Claude Code apply command: `/kc-ui use <style-id> <task>`
- Claude Code shorthand apply command: `/kc-ui <style-id> <task>`

## Examples

### Codex

```text
$kc-ui list
$kc-ui look agency-compact
$kc-ui use agency-compact redesign the settings page
$kc-ui agency-compact adjust the whole project UI
```

### Claude Code

```text
/kc-ui list
/kc-ui look agency-compact
/kc-ui use agency-compact redesign the settings page
/kc-ui agency-compact adjust the whole project UI
```

### Ambiguous request

```text
$kc-ui make the settings page dark and minimal
```

Expected behavior: do not edit code. Show the available style ids and ask the user to choose one explicitly, for example `$kc-ui use agency-compact make the settings page dark and minimal`.

## Workflow

### 1. Parse the command

- `list`: output all available style ids and one-line descriptions.
- `look <style-id>`: output the full style spec for the selected style.
- `use <style-id> <task>` or `<style-id> <task>`: apply that style to the current project UI.
- Missing style id, unknown style id, or generic natural-language style only: do not modify files; list available styles and expected usage.

### 2. Inspect the target project before editing

- Read the relevant UI files, theme tokens, component library, design system, and existing layout structure.
- Prefer existing project tokens, components, framework conventions, and utility classes.
- Identify whether the target is web, desktop, or mobile, then translate the selected style to that platform instead of copying a desktop layout everywhere.
- Before editing, state which files will change and why.

### 3. Apply the selected style

- Use the style spec as the source of truth for typography, density, colors, radius, component states, and layout rhythm.
- Keep product functionality unchanged unless the user's task explicitly asks for behavior changes.
- Do not invent new pages, fake data, or screenshot-only content when the task is a style transformation.
- Keep edits scoped to the requested page, component, or UI surface.

### 4. Verify

- Run the project's available typecheck, lint, build, or focused UI verification when practical.
- For visual work, inspect the result in the relevant viewport or app window when tools are available.
- Check scale specifically: body font, control height, sidebar width, padding, margin, card size, and titlebar alignment must match the selected style's density.

## Built-in Styles

### `agency-compact`

One-line description: dark, compact, macOS-native utility-app style with restrained orange accents, dense spacing, source-list navigation, and subtle surface layering.

#### Positioning

- Use for: settings screens, account/profile managers, control panels, dashboards, source-list apps, developer tools, utility apps, web admin panels, desktop apps, and mobile utility screens.
- Avoid for: marketing landing pages, image-heavy campaigns, game UI, brand storytelling pages, and large display/kiosk interfaces.
- Keywords: dark, compact, macOS-native, Apple-native, source-list, utility-app, minimal, dense, restrained, professional.

#### Typography

- Web and desktop root/base font size: `13px`.
- Body text, nav items, controls, table cells: `13px`.
- Secondary text and metadata: `12px`.
- Badges, labels, and small kicker text: `10px` to `11px`.
- List titles and titlebar labels: `14px`.
- Page, modal, or dialog titles: `18px`.
- Avoid default `16px`-heavy layouts unless the target platform requires it for accessibility; if used, preserve the compact visual density through spacing and hierarchy.

#### Colors

- Canvas: `#151516`.
- Titlebar or topbar: `#202023`.
- Sidebar or navigation surface: `#222224`.
- Main surface: `#1b1b1d`.
- Raised surface: `#242427`.
- Pressed surface: `#101011`.
- Control surface: `#1a1a1c`.
- Hover surface: `#29292d`.
- Border: `rgba(255,255,255,0.09)`.
- Strong border: `rgba(255,255,255,0.15)`.
- Primary text: `#e6e6e9`.
- Secondary text: `#aaaab1`.
- Muted text: `#85858d`.
- Accent orange: `#ff7a2f`.
- Success: `#48d17a`.
- Danger: `#ff6b68`.
- Warning: `#f5b85f`.

#### Sizing And Spacing

- Desktop titlebar, when the app owns one: about `38px`.
- Toolbar: `48px` to `54px`.
- Sidebar: `220px` to `236px`, and normally no more than `28%` of a `980px`-wide window.
- List rows: `56px` to `64px`.
- Buttons: `28px` to `34px`.
- Inputs and selects: `32px` to `36px`.
- Card and panel padding: `10px` to `16px`.
- Page padding: `16px` to `24px`.
- Prefer `4px`, `6px`, `8px`, `10px`, `12px`, `16px`, and `20px` spacing steps.

#### Radius

- Small controls: `8px`.
- Medium controls and rows: `11px`.
- Large panels: `16px`.
- Pills: `999px`.

#### Component Rules

- Use thin borders and subtle surface contrast instead of large shadows.
- Use hover transitions around `140ms` for background, border, opacity, and transform.
- Use pressed dark surfaces for active interactions.
- Use orange accents sparingly for primary actions, selected indicators, focus rings, and important status markers.
- Selected nav items or rows should use a subtle pressed background plus either a restrained accent tint or a `2px` orange indicator.
- Avoid oversized cards, heavy shadows, large whitespace, and decorative gradients unless the existing product already relies on them.

#### Platform Translation

- Web: use the full viewport. Do not wrap the whole page in a fake small desktop window. Translate the style into a full-width app shell with sidebar, topbar, content regions, or a responsive equivalent.
- Desktop: titlebar, sidebar, split panes, and content panels are appropriate. Prefer native platform controls when available. Do not render duplicate traffic-light controls if the shell already provides native window controls.
- Mobile: translate the style into compact headers, tabs or bottom navigation, sheets, compact cards, and dense lists. Do not copy the desktop sidebar directly onto mobile.

#### UI Scale Guardrails

- Do not infer CSS sizes directly from screenshot pixels. Account for Retina screenshots, browser zoom, and device pixel ratio.
- Prefer source tokens, design-system values, DevTools computed values, or explicit spec values from this skill.
- Do not default to a `16px` body with `20px+` controls for compact tool UI.
- If the result feels globally too large, first reduce root font, toolbar height, row height, padding, and sidebar width according to this style spec.

## Guardrails

- Never apply a style unless the command includes an explicit known style id.
- Never treat a generic request like "dark theme" as permission to choose a style automatically.
- Do not change product behavior while styling unless explicitly requested.
- Do not hand-edit generated `dist` files in `agent-deck`; edit `skills/<name>/source.md` and rerender.
- Keep every style cross-platform. A style can have platform-specific translation rules, but it must not be only a desktop, web, or mobile template.

## Output Templates

### `list`

```text
Available UI styles:
- agency-compact: dark, compact, macOS-native utility-app style with restrained orange accents.

Use:
- $kc-ui look agency-compact
- $kc-ui use agency-compact <task>
```

### Missing or ambiguous style id

```text
I need an explicit UI style id before changing code.

Available UI styles:
- agency-compact: dark, compact, macOS-native utility-app style with restrained orange accents.

Rerun with:
$kc-ui use agency-compact <task>
```

### `look agency-compact`

Return the full `agency-compact` spec from Built-in Styles, including positioning, typography, colors, sizing, radius, component rules, platform translation, and scale guardrails.
