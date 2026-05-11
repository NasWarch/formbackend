# ANIMATIONS.md — CoproMaintenance

## Motion Philosophy
Animations must clarify state, guide attention, or improve perceived speed.
No decorative motion that slows the UI or feels like "template animation."
Use **framer-motion** for complex animations, Tailwind transitions for simple ones.

## Timing
- Micro-interactions (hover, focus): `duration-150`
- State transitions (open/close): `duration-200`
- Page transitions: `duration-250`
- Modals/overlays: `duration-200`, ease-out for enter, ease-in for exit
- Default easing: `cubic-bezier(0.22, 1, 0.36, 1)` — crisp, not bouncy

## Required Motion

### Buttons and Controls
- **Hover**: `transition-colors duration-150` — background color change
- **Press**: `active:scale-[0.97]` on buttons — subtle micro-feedback
- **Focus**: ring animation via CSS `focus-visible:ring-2`
- **Disabled**: `opacity-50 cursor-not-allowed` — no animation needed
- **Loading**: `Loader2` with `animate-spin` replacing button text/icon

### Navigation
- **Sidebar active**: `bg-accent/50 text-accent-foreground font-medium` with `transition-colors duration-150`
- **Mobile menu**: slide from left with `framer-motion` `x: [-240, 0]`, `duration-200`
- **Tabs**: no animation needed — instant switch

### Data and Feedback
- **Loading states**: `Loader2 animate-spin` icon + fade in
- **Toast**: sonner default — slide from right, auto-dismiss
- **Modal**: framer-motion — scale from 0.95 + fade in overlay, `duration-200`
- **Form validation**: instant red border + message — no delay
- **Empty state**: simple render — no animation needed

### Product Moments
- **Create success**: toast notification
- **Data processing**: spinner in button during API call
- **Stats update**: no animation — instant refresh

## Framer Motion Defaults
```ts
const ease = [0.22, 1, 0.36, 1]
const transition = { duration: 0.2, ease }
```

## Restrictions
- No infinite decorative motion — only loading spinners
- No parallax/scroll effects in dashboards
- No animations that hide layout bugs
- Respect `prefers-reduced-motion` — `motion:reduce` in Tailwind
