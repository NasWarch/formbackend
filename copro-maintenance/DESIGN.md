# CoproMaintenance — Design System v2

> Direction artistique : **Stripe B2B premium** (confiance, clarté) + **Linear operational** (dashboards denses, efficaces)
> Palette : 70% neutres chauds / 20% sauge douce / 10% vert forêt profond

## 1. Visual Theme & Atmosphere

CoproMaintenance est un outil professionnel pour les syndics de copropriété.
Le design doit inspirer **confiance, sérieux et efficacité** — pas de "green-washing", pas de gradients génériques.

**Mood** : Propre, aéré, typographique. Beaucoup d'espace blanc, des cartes nettes, des ombres subtiles.
Le vert forêt profond (`#1a6d4a`) est utilisé avec parcimonie — uniquement pour les actions clés.
Le fond est un blanc légèrement chaud (`#fafafa`) qui évite la froideur des SaaS génériques.

**Éléments clés :**
- Police unique : **Inter** (système, excellent support français)
- Fond : blanc chaud `#fafafa` — plus agréable à lire que `#ffffff` pur
- Vert forêt profond `#1a6d4a` comme seul accent chromatique
- Vert très foncé `#0a2e1a` pour les titres — substance, pas d'agressivité
- Ombres multi-couches très subtiles : `0 1px 2px rgba(0,0,0,0.04)` et `0 1px 3px rgba(0,0,0,0.06)`
- Bordures légères `1px solid #e8e8e8` plutôt que hairline forte
- Arrondis 8px (md) pour les cards, 6px (sm) pour les inputs
- Transitions 150ms ease sur tous les interactifs

## 2. Color Palette

### 70% — Neutral / Background
| Token | Hex | Usage |
|-------|-----|-------|
| `canvas` | `#fafafa` | Page background (blanc chaud) |
| `canvas-pure` | `#ffffff` | Cards, modals, dropdowns |
| `surface` | `#f4f4f5` | Secondary sections, hover backgrounds |
| `surface-hover` | `#eaeaeb` | Hover sur cards/surface |
| `hairline` | `#e8e8e8` | Borders subtils |
| `hairline-strong` | `#d4d4d4` | Borders plus marqués |
| `text-primary` | `#18181b` | Titres, navigation |
| `text-body` | `#3f3f46` | Corps de texte |
| `text-muted` | `#71717a` | Labels discrets, captions |
| `text-subtle` | `#a1a1aa` | Placeholders, métadonnées |
| `text-disabled` | `#d4d4d4` | États désactivés |
| `icon-default` | `#71717a` | Icônes standards |
| `icon-muted` | `#a1a1aa` | Icônes secondaires |

### 20% — Secondary / Supporting
| Token | Hex | Usage |
|-------|-----|-------|
| `sage-light` | `#f0f7f4` | Badges backgrounds, cards sélectionnées |
| `sage-mid` | `#dce8e0` | Borders d'états OK, accents discrets |
| `sage-text` | `#2d6a4f` | Texte sur badges OK |
| `warm-sand` | `#faf6f0` | Background alternatif, alertes warning doux |
| `warm-stone` | `#f5f0eb` | Surfaces hover sur fond chaud |

### 10% — Accent / Action
| Token | Hex | Usage |
|-------|-----|-------|
| `accent` | `#1a6d4a` | Primary buttons, liens, focus rings |
| `accent-hover` | `#155a3d` | Hover primary |
| `accent-pressed` | `#0f4a30` | Pressed primary |
| `accent-ring` | `rgba(26,109,74,0.25)` | Focus rings |

### Semantic Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `success` | `#16a34a` | Conforme, OK |
| `success-bg` | `#f0fdf4` | Background badge OK |
| `warning` | `#d97706` | À prévoir |
| `warning-bg` | `#fffbeb` | Background badge warning |
| `error` | `#dc2626` | En retard, erreurs |
| `error-bg` | `#fef2f2` | Background badge erreur |
| `info` | `#2563eb` | Information |

### 70/20/10 Rule Application
```
[Background canvas]        70%  → #fafafa, #ffffff, #f4f4f5
[Borders, cards, badges]   20%  → #e8e8e8, #f0f7f4, #d4d4d4
[Buttons, links, accent]   10%  → #1a6d4a
```

**DO NOT use:**
- Gradients on backgrounds or buttons
- Purple or blue SaaS palette
- Green everywhere (reserve for accent only)
- Multiple saturated colors in one view

## 3. Typography

Font : **Inter Variable** (weights 300-700)

| Token | Size | Weight | Line H | Letter Sp | Usage |
|-------|------|--------|--------|-----------|-------|
| `h1` | 28px | 600 | 1.2 | -0.3px | Page titles |
| `h2` | 20px | 600 | 1.3 | -0.2px | Section titles |
| `h3` | 16px | 600 | 1.4 | 0 | Card titles |
| `h4` | 14px | 600 | 1.4 | 0 | Sub-card titles |
| `body` | 15px | 400 | 1.5 | 0 | Body text |
| `body-sm` | 14px | 400 | 1.5 | 0 | Small body |
| `caption` | 13px | 500 | 1.4 | 0 | Labels |
| `micro` | 12px | 500 | 1.4 | 0.3px | Meta, badges |
| `btn` | 14px | 500 | 1 | 0 | Buttons |
| `btn-sm` | 13px | 500 | 1 | 0 | Small buttons |
| `mono` | 13px | 400 | 1.5 | 0 | Code/mono |

## 4. Spacing

Base unit: 4px

| Token | Rem/Px |
|-------|--------|
| `xxs` | 4px |
| `xs` | 8px |
| `sm` | 12px |
| `md` | 16px |
| `lg` | 20px |
| `xl` | 24px |
| `xxl` | 32px |
| `xxxl` | 40px |
| `section` | 48px |
| `section-lg` | 64px |

## 5. Border Radius

| Token | Value |
|-------|-------|
| `sm` | 6px |
| `md` | 8px |
| `lg` | 12px |
| `xl` | 16px |
| `full` | 9999px |

## 6. Shadows

```css
/* Card (default) */
box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.06);

/* Card hover */
box-shadow: 0 4px 6px rgba(0,0,0,0.04), 0 2px 4px rgba(0,0,0,0.06);

/* Modal / dropdown */
box-shadow: 0 10px 15px rgba(0,0,0,0.06), 0 4px 6px rgba(0,0,0,0.05);

/* Elevated (pricing featured) */
box-shadow: 0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -4px rgba(0,0,0,0.04);
```

## 7. Component Architecture

### Buttons
| Variant | Style |
|---------|-------|
| `primary` | `bg-accent text-white`, md rounded, h-9, px-4 |
| `secondary` | `bg-surface text-text-body border hairline` |
| `ghost` | `bg-transparent text-text-body hover:bg-surface` |
| `destructive` | `bg-error text-white hover:bg-error/90` |
| `outline` | `bg-canvas-pure border hairline text-text-body hover:bg-surface` |
| `link` | `text-accent underline-offset-2 hover:underline` |
| States | hover → `accent-hover`, active → `accent-pressed`, loading → spinner + disabled |

### Cards
| Variant | Style |
|---------|-------|
| `default` | `bg-canvas-pure border hairline`, md rounded, p-xl |
| `hover` | Same + hover shadow transition |
| `stat` | bg-canvas-pure, border hairline, md rounded, p-lg, stat value in accent |

### Form Inputs
- Height 36px (sm) or 40px (md), sm rounded (`6px`)
- Border `hairline-strong`, focus `ring-2 accent-ring border-accent`
- Label: `text-sm font-medium text-text-body mb-1`
- Error: `border-error ring-error/30`
- Placeholder: `text-text-subtle`

### Badges
| Variant | Style |
|---------|-------|
| `ok` | `bg-success-bg text-success border-success/20` |
| `pending` | `bg-warning-bg text-warning border-warning/20` |
| `overdue` | `bg-error-bg text-error border-error/20` |

## 8. Layout Rules

### Dashboard Layout
```
[Sidebar 240px] + [Main Content]
   Icon + label     Top bar (search + user menu)
   Active state     Content area (cards, tables)
   accent bg        Scrollable
```

- Sidebar: fixed 240px, bg-canvas-pure, border-right hairline
- Top bar: h-14, bg-canvas-pure, border-b hairline
- Content: max-w-7xl, mx-auto, p-xl

### Landing Page
```
[Nav] → transparent, sticky, logo + links + CTA
[Hero] → centered, h1 + p + CTA + product screenshot
[Features] → 3x2 grid, icon + title + description
[How It Works] → 3 numbered steps
[CTA Final] → accent background, big CTA
[Footer] → links + copyright
```

## 9. CSS Custom Properties (globals.css)

```css
:root {
  --background: #fafafa;
  --foreground: #18181b;
  --card: #ffffff;
  --card-foreground: #18181b;
  --popover: #ffffff;
  --popover-foreground: #18181b;
  --primary: #1a6d4a;
  --primary-foreground: #ffffff;
  --secondary: #f4f4f5;
  --secondary-foreground: #3f3f46;
  --muted: #f4f4f5;
  --muted-foreground: #71717a;
  --accent: #f0f7f4;
  --accent-foreground: #155a3d;
  --destructive: #dc2626;
  --destructive-foreground: #ffffff;
  --border: #e8e8e8;
  --input: #d4d4d4;
  --ring: #1a6d4a;
  --radius: 0.5rem;
  --sidebar-width: 240px;
}
```

## 10. Design Principles

1. **Confiance d'abord** — Pas d'effets gratuits. Le design doit inspirer les professionnels de l'immobilier.
2. **Parcimonie de la couleur** — Le vert est réservé aux actions clés. 70% de neutres.
3. **Clarté réglementaire** — Les statuts de conformité lisibles en un coup d'œil (OK/warning/error).
4. **Mobile-ready** — Les syndics consultent depuis leur téléphone. Tables responsives, boutons tactiles.
5. **Français d'abord** — Interface 100% française, dates fr-FR, format français.
6. **Pas de features fantômes** — Si une fonctionnalité n'est pas implémentée, retirée ou marquée clairement.
7. **Accessibilité** — Contrastes WCAG AA, focus visibles, labels ARIA.
