# Breakpoint System

Senior Forge Codex consolidates the Chirpy theme's 6+ default breakpoints into **3 primary breakpoints** plus one visual threshold. All overrides live in `_includes/metadata-hook.html`.

## Breakpoint Map

| Breakpoint | Role | Zone below | Zone above |
|---|---|---|---|
| **600px** | Mobile → Tablet | Compact mobile layout | Comfortable tablet layout |
| **850px** | Tablet → Desktop | No sidebar, hamburger menu | Sidebar visible, desktop layout |
| **1200px** | Content reflow | Full-width content column | Content column narrowed (col-lg-11), TOC panel appears |
| **1650px** | Visual threshold only | Container fills available space | Container capped at 1320px (margins grow); glossary switches to 3 columns |

## Eliminated Breakpoints

These Chirpy/Bootstrap breakpoints are neutralized by overrides:

| Original | What it did | How it was eliminated |
|---|---|---|
| **1650px** (Chirpy) | Sidebar expanded to 350px, container max-width 1250px, padding changes | Override forces pre-1650 values (sidebar stays 310px, container stays 1320px, padding stays 12px) |
| **1400px** (Bootstrap XXL `px-xxl-5`) | Container padding jumped from 12px to 48px (3rem) | Override forces `padding: 12px` at ≥1400px |
| **992px** (Bootstrap LG `col-lg-11`) | Content column narrowed to 96% flex | Override forces `flex: 0 0 100%` in the 992–1199px range, so the effect only starts at 1200px |
| **768px** (Bootstrap MD) | Container went full-width with 0 padding | Override preserves `max-width: none` and 12px padding in the 601–768px range, so the real shift happens at 600px |

## What Happens at Each Breakpoint

### ≤599px — Compact Mobile

- **Sidebar:** Hidden off-screen (translateX). Hamburger menu visible.
- **Breadcrumb:** Hidden (Chirpy default below 850px).
- **Container:** Full-width (`max-width: none`), zero side padding.
- **Content padding:** 1rem (16px) left/right on `main` and `#topbar-wrapper` (same as 600–849px — no jump at 600px).
- **Glossary cards:** 1 column.
- **Glossary search results:** 1 column.
- **Global search results (sidebar):** 1 column.
- **Tag pages (`/en/tags/<tag>/`, `/es/etiquetas/<tag>/`):** 1 column.

### 600px — Mobile to Tablet

- **Content padding:** Stays at 1rem (16px) — no change from below 600px (only column count changes).
- **Glossary cards:** Switch from 1 to 2 columns.
- **Glossary search results:** Switch from 1 to 2 columns.
- **Global search results (sidebar):** Switch from 1 to 2 columns.
- **Tag pages:** Switch from 1 to 2 columns.

### 850px — Tablet to Desktop

- **Sidebar:** Becomes visible (fixed, 310px wide via `--sidebar-width`).
- **Main wrapper:** Gets `margin-left: 310px` to make room for sidebar.
- **Breadcrumb:** Becomes visible. Full text shown (truncation prevented up to 1199px via override).
- **Topbar:** Consistent 24px left/right padding at all desktop widths (overrides Bootstrap's `px-lg-3` which would have added different padding at 992px).
- **Content padding:** Controlled by Bootstrap column gutter (24px).
- **Hamburger menu:** Hidden.
- **Global search results (sidebar):** Stays at 2 columns.

### 1200px — Content Reflow

- **Content column:** Narrows from 100% to ~96% (`col-lg-11` flex takes effect here instead of at 992px).
- **Breadcrumb:** Chirpy's truncation override no longer needed (theme stops truncating above 1200px natively).
- **TOC panel:** Appears in the right margin (Chirpy default).
- **Font size:** Chirpy increases base font size.
- **Global search results (sidebar):** Switch from 2 to 3 columns.

### 1650px — Visual Threshold

Not a layout breakpoint — the container is capped at 1320px so margins grow symmetrically as the viewport widens.

- **Sidebar:** Stays at 310px (Chirpy would have expanded to 350px).
- **Container:** Stays at `max-width: 1320px` with 12px padding (Chirpy would have changed to 1250px with different padding).
- **Global search results (sidebar):** Stays at 3 columns; lateral space grows, card width constant.
- **Glossary cards:** Switch from 2 to 3 columns.
- **Glossary search results:** Switch from 2 to 3 columns.
- **All sidebar internal spacing:** Frozen at pre-1650 values (profile, nav items, bottom icons).
- **Tag pages:** Switch from 2 to 3 columns.

## File Reference

| File | What it controls |
|---|---|
| `_includes/metadata-hook.html` | All breakpoint overrides (CSS `@media` rules with `!important`) |
| `_includes/search-loader.html` | Global search results grid (sidebar search): column breakpoints and card styles |
| `en/glossary/index.md` | Glossary search result grid breakpoints (inline `<style>`) |
| `es/glosario/index.md` | Same as above, Spanish version |
| `_layouts/tag.html` | Tag page card grid breakpoints (inline `<style>`), same thresholds as the glossary grid |

## Design Decisions

1. **Why 600px instead of 768px for mobile?** The 768px breakpoint is too wide for modern phones — content still looks fine in a single column up to 600px. This gives tablets a two-column glossary earlier.

2. **Why neutralize 1400px and 1650px instead of removing them?** The CSS comes from the Chirpy gem (read-only). Overrides with `!important` are the only option without forking the theme.

3. **Why 24px topbar padding?** Matches Bootstrap's column gutter (`calc(var(--bs-gutter-x) * .5) = 24px`), keeping the breadcrumb aligned with body text at all desktop widths. The ~4px visual offset from the text start is acceptable.

4. **Why prevent breadcrumb truncation at 850–1199px?** Chirpy truncates the breadcrumb to 65% width with `text-overflow: ellipsis` in this range. With a fixed sidebar, there's enough horizontal space to show the full breadcrumb path.

5. **Why 3 columns at 1650px?** The container stops growing at this point (capped at 1320px), so the extra width comes as side margins. Switching to 3 glossary columns uses the available container width more effectively at this natural visual threshold.
