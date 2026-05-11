<div align="center">
  <h1>FormBackend API</h1>
  <p><strong>Open-core self-hosted form backend. Deploy in 10 seconds.</strong></p>
  <p>Stop writing backend code for your HTML forms. One endpoint URL, submissions arrive in your dashboard, notifications on your channel.</p>

  <p>
    <a href="#-quick-start"><img src="https://img.shields.io/badge/Try_in_1_minute-%238B5CF6?style=for-the-badge" alt="Try in 1 minute"></a>
    <a href="https://github.com/NasWarch/formbackend"><img src="https://img.shields.io/github/stars/NasWarch/formbackend?style=for-the-badge&logo=github" alt="GitHub stars"></a>
    <a href="https://github.com/NasWarch/formbackend/actions"><img src="https://img.shields.io/github/actions/workflow/status/NasWarch/formbackend/ci.yml?style=for-the-badge&logo=githubactions&label=build" alt="Build"></a>
    <a href="https://hub.docker.com/r/naswarch/formbackend"><img src="https://img.shields.io/docker/pulls/naswarch/formbackend?style=for-the-badge&logo=docker" alt="Docker pulls"></a>
  </p>
</div>

---

## 📸 Demo

![FormBackend API Demo](.github/images/formbackend-demo.gif)

*A 10-second walkthrough: deploy → create form → submit data → receive confirmation.*

---

## 🚀 Quick Start

**Deploy with one command:**

```bash
git clone https://github.com/NasWarch/formbackend.git
cd formbackend
cp .env.example .env  # edit if you want custom secrets
docker compose up -d
```

Open **http://localhost:8000**, sign up with your email (magic link — no password needed), create a form, and paste the endpoint URL into any HTML form.

That's it. Submissions appear in your dashboard in real-time.

---

## ✨ Features

| Feature | Free | Starter (8€) | Pro (19€) | Business (39€) |
|---------|------|-------------|-----------|----------------|
| Submissions/month | 50 | 500 | 2,000 | 10,000 |
| Forms | 1 | 5 | 20 | Unlimited |
| REST API endpoint | ✅ | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ✅ | ✅ | ✅ |
| Email notifications | — | ✅ | ✅ | ✅ |
| Slack / Discord / Webhook | — | — | ✅ | ✅ |
| SMS notifications | — | — | — | ✅ |
| Anti-spam (honeypot) | ✅ | ✅ | ✅ | ✅ |
| Anti-spam (reCAPTCHA) | — | — | ✅ | ✅ |
| Custom CORS | — | ✅ | ✅ | ✅ |
| Custom domain | — | — | — | ✅ |
| White label | — | — | — | ✅ |
| CSV / JSON export | ✅ | ✅ | ✅ | ✅ |
| Data retention | 30 days | 90 days | 365 days | Forever |
| Team members | — | — | — | Up to 5 |
| API access | — | ✅ | ✅ | ✅ |
| Zapier / Make integrations | — | — | — | ✅ |

---

## 📊 Why FormBackend?

| vs | Formspree | Web3Forms | Formcarry | **FormBackend** |
|---|---|---|---|---|
| Free tier | 50 sub/mo | 100 sub/mo | 100 sub/mo | **50 sub/mo** |
| Entry plan | $8/mo — 50 sub | $9/mo — 1,000 sub | $12/mo — 1,000 sub | **8€/mo — 500 sub** |
| Mid plan | $18/mo — 500 sub | — | — | **19€/mo — 2,000 sub** |
| Top plan | $55/mo — 2,500 sub | $29/mo — 5,000 sub | $24/mo — 3,000 sub | **39€/mo — 10,000 sub** |
| Self-hostable | ❌ Proprietary | ❌ Proprietary | ❌ Proprietary | **✅ Open-core** |
| Anti-spam advanced | ❌ | ❌ | ❌ | **✅ reCAPTCHA + honeypot** |
| Multi-channel notif | ❌ | ❌ | ❌ | **✅ Slack, Discord, SMS** |
| Custom domain | $12/mo extra | ❌ | ❌ | **✅ Included Business** |
| White label | ❌ | ❌ | ❌ | **✅ Included Business** |
| Pricing in EUR | ❌ ($) | ❌ ($) | ❌ ($) | **✅** |

**The short version:** 10× more submissions than Formspree at the same price, self-hostable, and more features at every tier.

---

## 🐳 Self-hosting

### docker-compose.yml

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15-alpine
    container_name: formbackend-db
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: formbackend
      POSTGRES_USER: formbackend
      POSTGRES_PASSWORD: change-me
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U formbackend"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: formbackend-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    image: ghcr.io/naswarch/formbackend:latest
    build: ./backend
    container_name: formbackend-api
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      DATABASE_URL: postgresql://formbackend:change-me@postgres:5432/formbackend
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET: generate-a-random-64-char-string
      SMTP_HOST: ""
      SMTP_PORT: "587"
      SMTP_USER: ""
      SMTP_PASS: ""
      SMTP_FROM: "noreply@yourdomain.com"
      CORS_ORIGINS: "*"
      RATE_LIMIT: "10/minute"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
```

### Run it

```bash
docker compose up -d
# Open http://localhost:8000
```

### Upgrade

```bash
docker compose pull backend
docker compose up -d
```

### Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ | — | PostgreSQL connection string |
| `REDIS_URL` | ✅ | — | Redis connection string |
| `JWT_SECRET` | ✅ | — | 64+ char random string for JWT signing |
| `SMTP_HOST` | ❌ | — | SMTP server for email notifications |
| `SMTP_PORT` | ❌ | 587 | SMTP port |
| `SMTP_USER` | ❌ | — | SMTP username |
| `SMTP_PASS` | ❌ | — | SMTP password |
| `SMTP_FROM` | ❌ | noreply@localhost | From address for notification emails |
| `CORS_ORIGINS` | ❌ | * | Comma-separated allowed origins |
| `RATE_LIMIT` | ❌ | 10/minute | Rate limit for form submission endpoint |
| `STRIPE_SECRET_KEY` | ❌ | — | Stripe secret key (for paid plans) |
| `STRIPE_WEBHOOK_SECRET` | ❌ | — | Stripe webhook signing secret |

---

## 💰 Pricing

| Plan | Price | Submissions | Forms | Best for |
|------|-------|-------------|-------|----------|
| **Free** | **0€** | 50/mo | 1 | Testing & prototypes |
| **Starter** | **8€/mo** | 500/mo | 5 | Solo devs & blogs |
| **Pro** | **19€/mo** | 2,000/mo | 20 | SMEs & agencies |
| **Business** | **39€/mo** | 10,000/mo | Unlimited | Scaling SaaS & teams |

> **Self-hosted users** get all Pro features for free + unlimited submissions. Business features (custom domain, white label, team) are included at the hosted Business tier.

---

## 🧩 API

### Submit form data

```http
POST /api/f/{endpoint}
Content-Type: application/x-www-form-urlencoded

name=John&email=john@example.com&message=Hello
```

**Response:**

```json
{
  "success": true,
  "message": "Formulaire soumis avec succès",
  "id": "a1b2c3d4"
}
```

### Anti-spam

Add a hidden `_gotcha` field to your form — if a bot fills it, the submission is silently accepted but not stored:

```html
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
```

---

## 🏗 Architecture

```
┌─────────────┐     ┌────────────┐     ┌──────────────┐
│   Browser    │────▶│  FastAPI   │────▶│  PostgreSQL  │
│  (HTML form) │     │  (uvicorn) │     │   (storage)  │
└─────────────┘     │            │     └──────────────┘
                    │            │     ┌──────────────┐
┌─────────────┐     │ Dashboard  │────▶│    Redis     │
│   Your app   │────▶│  (HTMX)   │     │ (sessions /  │
│ (JavaScript) │     └────────────┘     │  rate limit) │
└─────────────┘                        └──────────────┘
                                               │
                                        ┌──────┴──────┐
                                        │  Notifications│
                                        │ Email / Slack│
                                        │ Discord / SMS│
                                        └─────────────┘
```

- **Backend:** Python 3.11 + FastAPI (async-first, production-grade)
- **Frontend:** HTMX + Jinja2 (zero build step, served directly)
- **Database:** PostgreSQL 15 (JSONB for submission data)
- **Cache:** Redis 8 (rate limiting, session store, webhook queue)
- **Auth:** Magic-link based JWT (no passwords to store)

---

## 🛠 Development

```bash
# Clone
git clone https://github.com/NasWarch/formbackend.git
cd formbackend

# Set up
cp .env.example .env
# Edit .env with your database credentials

# Run locally (requires PostgreSQL + Redis)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with Docker
docker compose up -d
```

### Run tests

```bash
cd backend
pip install -r requirements.txt
pip install pytest httpx
pytest tests/ -v
```

---

## 🤝 Contributing

PRs welcome! Check the [open issues](https://github.com/NasWarch/formbackend/issues) for things to work on.

**Stack:** Python 3.11, FastAPI, SQLAlchemy, HTMX, Docker.

---

## 📄 License

[AGPL-3.0](LICENSE) — Free to use, modify, and self-host. Commercial use requires a paid license for hosted deployments with >50 monthly submissions.

---

<div align="center">
  <p>Built with ❤️ for developers who hate reinventing the wheel.</p>
  <p>
    <a href="https://github.com/NasWarch/formbackend">GitHub</a> ·
    <a href="#-quick-start">Quick Start</a> ·
    <a href="#-pricing">Pricing</a> ·
    <a href="https://github.com/NasWarch/formbackend/issues">Issues</a>
  </p>
</div>
