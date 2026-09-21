# UI_UX_DESIGN_SYSTEM.md

## Scope and a copyright note
The request was to "clone" wise.com. **This documents an original design system inspired by Wise's publicly documented visual language (color roles, type roles, radius/elevation system) — not a literal clone.** Wise's actual site code, copy, logo, illustrations, and proprietary "Wise Sans" typeface are their IP and are not reproduced here. What's reused is the *pattern* (a restrained single-accent color system, a two-typeface role split, pill/rounded-card geometry) applied to ClaimLens Nexus's own content and its own insurance-analytics subject matter, with a free substitute typeface. This is the same relationship a design brief has to "in the style of a Scandinavian fintech" — a direction, not a copy.
Go to wise.com and prepare an exact section, detailed copy, but for our website. Just content change.

## Design tokens

### Color
```
--canvas:        #EEF4E8   Pale sage-tinted page background (Wise-language: light canvas, not dark)
--surface:        #FFFFFF   White cards floating on canvas
--ink:            #10130E   Near-black text with a faint warm undertone
--brand-lime:     #9FE870   Single accent — CTAs, primary badges, active states ONLY (never decorative filler)
--forest:         #163300   Dark green — text-on-lime, header/hero band, dark UI moments
--sage-tint:      #E2F6D5   Soft highlight fill (badge backgrounds, hover states)
--line:           rgba(16,19,14,0.12)   Hairline ring borders instead of soft drop shadows
```
Two semantic additions, kept deliberately minor since the reference system uses one accent color as "voltage" — these are status-only, never used for brand/CTA:
```
--status-insight:  #C98A2E  (muted amber) — INSIGHT badges, anomaly flags
--status-risk:     #B3452F  (muted brick-red) — high anomaly-score rows only
```

### Type
```
Display:  Inter, weight 800–900, line-height ~0.9 — hero KPI numbers, page title
Body/UI:  Inter, weight 500–600 default (not 400 — a confident, non-light default
          is part of the reference system's voice), 400 for long-form paragraph text
```
Inter substitutes for the reference system's proprietary display face — it's freely licensed, available via Google Fonts, and supports the same heavy weights.

### Shape / elevation
```
Buttons:   fully rounded (pill), scale(1.03) on hover instead of a color change
Cards:     24–30px radius
Elevation: a single 1px ring (var(--line)), not a soft blur shadow — this is the
           system's actual "material" language: contrast between flat surfaces,
           not depth via shadow
```

## Design plan (per frontend-design process: plan → review against brief → build)
**Color:** canvas #EEF4E8, surface #FFFFFF, ink #10130E, brand-lime #9FE870, forest #163300, sage-tint #E2F6D5.
**Type:** Inter 900 for display, Inter 600 for UI labels/body-emphasis, Inter 400 for body copy.
**Layout:** left-aligned content, bold hero KPI band up top (the one place boldness is spent), then a calm two-column body — review queue + chart on the left, Ask ClaimLens + Decision Log + external context on the right. Not a symmetric SaaS-card grid — the KPI band is visually heavier than everything below it, on purpose.
**Principles:** one accent color used sparingly and consistently (never recolored per status — status uses its own muted, separate palette); insight vs. decision is a *visual* system, not just a badge — insights live in lime/amber, decisions live in a visually distinct log with its own treatment; numbers are the hero, not chrome around them.

**Self-check against the generic-AI-design defaults** (per frontend-design skill): avoided warm-cream+terracotta, avoided all-caps eyebrows and em-dash labels, avoided uniform SaaS-card-kit shadows (used the ring-border approach instead), avoided arrow-suffixed CTAs. The dominant canvas is light, not dark-with-acid-accent, which keeps this out of that specific AI-design tell despite using a bright green accent.

## Component inventory used in the dashboard concept (shadcn-influenced, hand-built for HTML/CSS since this is a published static page)
- **KPI stat card** — large number, small label, no icon clutter
- **Badge** — pill-shaped, two variants: `insight` (amber) and `decision` (forest/lime), never interchangeable
- **Data table row** — ranked review queue, with an inline anomaly-score mini-bar
- **Tabs** — line-of-business filter on the trend chart
- **Search/query input** — Ask ClaimLens bar, pill-shaped, lime focus ring
- **Card** — white surface, 1px ring, 24px radius, used for every content block
- **Log entry** — Decision Log strip, visually distinct from insight badges (forest background, not lime) to keep the insight/decision line legible at a glance

## PENDING — cannot be documented without the original plan
Exact 8-page inventory, component-level states beyond what's modeled in the dashboard concept, exact responsive breakpoints named in the original plan.

See the published dashboard concept for this system applied to real ClaimLens Nexus content (Executive Overview page).
