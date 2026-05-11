# CoproMaintenance — Implementation Plan

> Build d'un SaaS B2B pour la gestion de maintenance des copropriétés françaises.

**Stack** : FastAPI + SQLAlchemy + SQLite (backend) / Next.js 14 + Tailwind + shadcn/ui (frontend)

---

## Task 1: Backend Foundation

**Objectif** : Mettre en place le projet FastAPI avec tous les modèles, core config, database, security.

- `/backend/app/main.py` — FastAPI app with lifespan, CORS, routes
- `/backend/app/__init__.py` — empty
- `/backend/app/core/__init__.py` — empty
- `/backend/app/core/config.py` — Settings (DB URL, JWT secret, CORS origins)
- `/backend/app/core/database.py` — Async SQLAlchemy engine + session + init_db()
- `/backend/app/core/security.py` — JWT create/verify, password hashing, get_current_user
- `/backend/app/models/__init__.py` — empty
- `/backend/app/models/user.py` — User (id, email, password_hash, name, company, plan, created_at)
- `/backend/app/models/building.py` — Building (id, user_id, name, address, city, postal_code, nb_lots, created_at)
- `/backend/app/models/equipment.py` — Equipment (id, building_id, name, type [ascenseur/chaudière/extincteur/porte/gaz/électricité/autre], serial_number, installation_date, last_control_date, next_control_date, status [ok/pending/overdue])
- `/backend/app/models/maintenance_record.py` — MaintenanceRecord (id, equipment_id, control_date, next_control_date, provider_name, status [ok/issue], notes, document_id nullable, created_at)
- `/backend/app/models/document.py` — Document (id, equipment_id, filename, original_name, content_type, size, uploaded_at)

## Task 2: Backend API Routes

**Objectif** : Tous les CRUD + auth endpoints.

- `/backend/app/api/__init__.py` — empty
- `/backend/app/api/auth.py` — POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
- `/backend/app/api/buildings.py` — GET/POST/PUT/DELETE /api/buildings
- `/backend/app/api/equipment.py` — GET/POST/PUT/DELETE /api/equipment
- `/backend/app/api/maintenance.py` — GET/POST /api/maintenance, GET /api/equipment/{id}/records
- `/backend/app/api/documents.py` — POST upload, GET download
- `/backend/app/api/dashboard.py` — GET /api/dashboard/summary (stats par immeuble)

## Task 3: Frontend Foundation

**Objectif** : Projet Next.js, shadcn/ui, layout, auth pages.

- Next.js 14 project with app router
- Tailwind config with CoproMaintenance theme (green palette from DESIGN.md)
- shadcn/ui setup (Button, Card, Input, Badge, Sheet, Table, Tabs, Calendar)
- `/frontend/app/layout.tsx` — Root layout with Inter font
- `/frontend/app/globals.css` — Tailwind + shadcn CSS variables
- `/frontend/lib/api.ts` — Axios/fetch wrapper with JWT token handling
- `/frontend/app/(auth)/login/page.tsx` — Login form
- `/frontend/app/(auth)/register/page.tsx` — Register form
- `/frontend/app/(auth)/layout.tsx` — Auth layout (centered card)

## Task 4: Frontend Dashboard

**Objectif** : Dashboard principal avec sidebar, vue immeubles, équipements.

- `/frontend/components/dashboard/Sidebar.tsx` — Navigation sidebar
- `/frontend/components/dashboard/Header.tsx` — Top bar with user menu
- `/frontend/app/(dashboard)/layout.tsx` — Dashboard layout (sidebar + header + content)
- `/frontend/app/(dashboard)/page.tsx` — Dashboard home avec summary stats cards
- `/frontend/app/(dashboard)/buildings/page.tsx` — Buildings list with add button
- `/frontend/app/(dashboard)/buildings/[id]/page.tsx` — Building detail: equipments list by category
- `/frontend/app/(dashboard)/buildings/[id]/equipment/new/page.tsx` — Add equipment form
- `/frontend/app/(dashboard)/equipment/[id]/page.tsx` — Equipment detail + maintenance history

## Task 5: Frontend Features

**Objectif** : Calendrier, upload documents, conformité.

- `/frontend/app/(dashboard)/calendar/page.tsx` — Calendar view of upcoming controls
- `/frontend/components/dashboard/CalendarView.tsx` — Month view calendar component
- `/frontend/app/(dashboard)/documents/page.tsx` — Document list/download
- `/frontend/components/dashboard/DocumentUpload.tsx` — Upload component with progress
- `/frontend/components/dashboard/ComplianceBadge.tsx` — Badge component for status
- `/frontend/app/(dashboard)/buildings/[id]/compliance/page.tsx` — Compliance overview by building

## Task 6: Landing Page & Pricing

**Objectif** : Site vitrine marketing.

- `/frontend/app/(landing)/page.tsx` — Landing page with hero, features, how it works
- `/frontend/app/(landing)/pricing/page.tsx` — Pricing page with 3 tiers
- `/frontend/app/(landing)/layout.tsx` — Landing layout (public nav + footer)
- `/frontend/components/landing/Hero.tsx` — Hero section
- `/frontend/components/landing/Features.tsx` — Features grid
- `/frontend/components/landing/PricingCards.tsx` — Pricing cards
- `/frontend/components/landing/Footer.tsx` — Footer

## Task 7: DevOps & Configuration

**Objectif** : Scripts de démarrage, tests, déploiement.

- `/backend/requirements.txt` — Python deps (fastapi, uvicorn, sqlalchemy, aiosqlite, python-jose, passlib, python-multipart, aiofiles)
- `/frontend/package.json` — Already from Next.js init
- `/frontend/.env.local` — API URL
- `/backend/start.sh` — Start backend script
- `/frontend/start.sh` — Start frontend script
- Docker compose optionnel
