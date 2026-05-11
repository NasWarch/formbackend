# COMPONENTS.md — CoproMaintenance

## Source
- Product: CoproMaintenance — Gestion maintenance copropriétés
- Project folder: `/root/monetization-lab/copro-maintenance`
- Design source: Stripe B2B + Linear operational
- Stack: Next.js 16 + Tailwind + shadcn/ui + lucide-react + framer-motion

## Component Principles
- Components match DESIGN.md v2 (70/20/10 palette, Inter font, green accent)
- Every interactive component has hover, focus, active, disabled states
- Core components have empty/loading/error states
- No dead buttons — every visible action either works or is explicitly disabled
- CSS variables from globals.css — no hardcoded colors

## Core Components

### App Shell
- **Sidebar**: fixed 240px, `bg-card border-r`, nav items with active accent bg
- **Top bar**: h-14, `bg-card border-b`, user menu with dropdown
- **Mobile nav**: Drawer/sheet on hamburger, same items as sidebar
- **Breadcrumbs**: `text-sm text-muted-foreground`

### Buttons (shadcn/ui Button)
- Primary: `bg-primary text-primary-foreground hover:bg-primary/90`
- Secondary: `bg-secondary text-secondary-foreground hover:bg-secondary/80`
- Ghost: `hover:bg-accent hover:text-accent-foreground`
- Destructive: `bg-destructive text-destructive-foreground hover:bg-destructive/90`
- Outline: `border border-input bg-background hover:bg-accent hover:text-accent-foreground`
- Link: `text-primary underline-offset-4 hover:underline`
- Icon button: `h-8 w-8 [&_svg]:size-4`, ghost variant
- Loading: show `Loader2` spinner + `disabled`
- All transitions: `transition-colors duration-150`

### Forms (shadcn/ui primitives)
- Input: `h-9 rounded-md border border-input bg-background px-3 py-1 text-sm`
  - Focus: `ring-2 ring-ring/30 border-ring`
  - Error: `border-destructive ring-destructive/30`
  - Placeholder: `text-muted-foreground`
- Textarea: same rules as input, `min-h-[80px]`
- Select: shadcn Select with same input styling
- Labels: `text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70`
- Error messages: `text-sm text-destructive mt-1`
- Success feedback: green border + check icon

### Data Display
- **Table**: shadcn Table, `w-full`, responsive scroll `overflow-x-auto`
  - Header: `text-xs font-medium text-muted-foreground uppercase tracking-wider`
  - Row hover: `hover:bg-muted/50`
- **Card**: `rounded-lg border bg-card text-card-foreground shadow-sm p-6`
- **Stat Card**: same as card, value in `text-2xl font-bold tracking-tight`, icon in accent tint bg
- **Badge**: `inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium`
  - ok: `bg-[#f0fdf4] text-[#16a34a]`
  - pending: `bg-[#fffbeb] text-[#d97706]`
  - overdue: `bg-[#fef2f2] text-[#dc2626]`
- **Empty state**: icon (48px) + title + description + optional CTA button
- **Loading state**: `Loader2` spinner centered + subtle text
- **Error state**: alert icon + message + Retry button

### Feedback
- **Toast**: sonner toast
- **Inline alert**: `rounded-lg border px-4 py-3 text-sm`
  - error: `bg-destructive/10 border-destructive/20 text-destructive`
  - success: `bg-[#f0fdf4] border-[#16a34a]/20 text-[#16a34a]`
- **Modal/Dialog**: shadcn Dialog, `sm:max-w-md`
  - Overlay: `bg-black/50`
  - Content: `bg-card p-6 shadow-lg rounded-lg`

### Product-Specific Components
- **ComplianceBadge**: Shows status (ok/pending/overdue) with icon + label
  - Props: `status: 'ok' | 'pending' | 'overdue'`
  - States: all 3 variants, each with icon + color
- **StatsCard**: Metric display tile
  - Props: `title, value, description?, icon, trend?`
  - States: normal, loading (skeleton)
- **AddControlDialog**: Modal for adding a maintenance record
  - Fields: control_date, next_control_date, provider_name, status, notes

## Accessibility
- Keyboard navigation: all interactive elements reachable via Tab
- Focus visibility: `focus-visible:ring-2 focus-visible:ring-ring`
- ARIA: `role`, `aria-label`, `aria-current="page"` on nav items
- Color contrast: WCAG AA minimum (4.5:1 for text, 3:1 for large text)

## Anti-Patterns
- No hardcoded colors — use Tailwind CSS variables (`bg-card`, `text-muted-foreground`)
- No dead buttons — every button must work or be `disabled` with explanation
- No forms without validation — client-side + server-side
- No nested cards inside cards — use list items or table rows instead
- No generic purple-blue gradients — use the green accent sparingly
