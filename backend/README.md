# OpenClaw Concierge Backend

FastAPI-based backend with a plugin system for managing concerts, events, news, and career data.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   ```

3. Create admin user:
   ```bash
   uv run python setup_admin.py
   ```

4. Run server:
   ```bash
   uv run uvicorn main:app --reload --port 5000
   ```

## API Authentication

Two authentication methods:
- **JWT Token**: `Authorization: Bearer <token>` (for dashboard users)
- **API Key**: `X-API-Key: <api-key>` (for data ingestion)

## Curl Examples

Set your environment variables:
```bash
export CONCIERGE_API_URL="http://localhost:5000/api"
export CONCIERGE_API_KEY="your-api-key"
```

---

### Authentication

**Login:**
```bash
curl -X POST "$CONCIERGE_API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

---

### Concerts

**Add a concert:**
```bash
curl -X POST "$CONCIERGE_API_URL/concerts" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "artists": ["Artist 1", "Artist 2"],
    "date": "2026-09-25",
    "venue": "Venue Name",
    "city": "Worcester, MA",
    "source_url": "https://tickets.example.com"
  }'
```

**List concerts:**
```bash
curl "$CONCIERGE_API_URL/concerts?page=1&per_page=20&upcoming=true" \
  -H "Authorization: Bearer $TOKEN"
```

**Get concert by ID:**
```bash
curl "$CONCIERGE_API_URL/concerts/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Update concert:**
```bash
curl -X PUT "$CONCIERGE_API_URL/concerts/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"venue": "New Venue Name"}'
```

**Delete concert:**
```bash
curl -X DELETE "$CONCIERGE_API_URL/concerts/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Prune past concerts:**
```bash
curl -X POST "$CONCIERGE_API_URL/concerts/prune" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

---

### Events

**Add an event:**
```bash
curl -X POST "$CONCIERGE_API_URL/events" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Event Title",
    "date": "2026-09-25",
    "city": "Boston, MA",
    "category": "exhibition",
    "summary": "Brief description",
    "source_url": "https://event.example.com"
  }'
```

**List events:**
```bash
curl "$CONCIERGE_API_URL/events?page=1&per_page=20&upcoming=true" \
  -H "Authorization: Bearer $TOKEN"
```

**Get event by ID:**
```bash
curl "$CONCIERGE_API_URL/events/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Update event:**
```bash
curl -X PUT "$CONCIERGE_API_URL/events/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Updated Title"}'
```

**Delete event:**
```bash
curl -X DELETE "$CONCIERGE_API_URL/events/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Prune past events:**
```bash
curl -X POST "$CONCIERGE_API_URL/events/prune" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

---

### News

**Add a news article:**
```bash
curl -X POST "$CONCIERGE_API_URL/news" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Article Title",
    "date": "2026-03-16",
    "category": "AI & Tech",
    "summary": "Brief summary of the article",
    "source_url": "https://news.example.com/article",
    "confirmed": false,
    "tags": ["ai", "technology"]
  }'
```

**List news:**
```bash
curl "$CONCIERGE_API_URL/news?page=1&per_page=20&unsent=true" \
  -H "Authorization: Bearer $TOKEN"
```

**Get news by ID:**
```bash
curl "$CONCIERGE_API_URL/news/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Update news:**
```bash
curl -X PUT "$CONCIERGE_API_URL/news/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"confirmed": true}'
```

**Delete news:**
```bash
curl -X DELETE "$CONCIERGE_API_URL/news/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Pop news (drip feed):**
```bash
curl -X POST "$CONCIERGE_API_URL/news/pop" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

**Prune news (mark all as sent):**
```bash
curl -X POST "$CONCIERGE_API_URL/news/prune" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

---

### Jobs

**Add a job:**
```bash
curl -X POST "$CONCIERGE_API_URL/careers/jobs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Senior Software Engineer",
    "company": "Acme Corp",
    "location": "Boston, MA",
    "salary_min": 150000,
    "salary_max": 200000,
    "job_url": "https://jobs.example.com/12345",
    "site": "linkedin",
    "date_posted": "2026-03-16",
    "is_remote": true,
    "summary": "Brief summary"
  }'
```

**List jobs:**
```bash
curl "$CONCIERGE_API_URL/careers/jobs?page=1&per_page=20&unsent=true" \
  -H "Authorization: Bearer $TOKEN"
```

**Get job by ID:**
```bash
curl "$CONCIERGE_API_URL/careers/jobs/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Update job:**
```bash
curl -X PUT "$CONCIERGE_API_URL/careers/jobs/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"salary_max": 220000}'
```

**Delete job:**
```bash
curl -X DELETE "$CONCIERGE_API_URL/careers/jobs/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Pop job (drip feed):**
```bash
curl -X POST "$CONCIERGE_API_URL/careers/jobs/pop" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

---

### Companies

**Add company research:**
```bash
curl -X POST "$CONCIERGE_API_URL/careers/companies" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Company Name",
    "location": "San Francisco, CA",
    "url": "https://company.example.com",
    "research_date": "2026-03-16",
    "research": "# Company Research\n\nMarkdown notes about the company..."
  }'
```

**List companies:**
```bash
curl "$CONCIERGE_API_URL/careers/companies?page=1&per_page=20" \
  -H "Authorization: Bearer $TOKEN"
```

**Get company by ID:**
```bash
curl "$CONCIERGE_API_URL/careers/companies/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Update company:**
```bash
curl -X PUT "$CONCIERGE_API_URL/careers/companies/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"research": "# Updated Research\n\nNew notes..."}'
```

**Delete company:**
```bash
curl -X DELETE "$CONCIERGE_API_URL/careers/companies/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### API Keys (Admin Only)

**List API keys:**
```bash
curl "$CONCIERGE_API_URL/api-keys" \
  -H "Authorization: Bearer $TOKEN"
```

**Create API key:**
```bash
curl -X POST "$CONCIERGE_API_URL/api-keys" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "My API Key"}'
```

**Update API key:**
```bash
curl -X PUT "$CONCIERGE_API_URL/api-keys/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Renamed Key", "is_active": true}'
```

**Delete API key:**
```bash
curl -X DELETE "$CONCIERGE_API_URL/api-keys/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Regenerate API key:**
```bash
curl -X POST "$CONCIERGE_API_URL/api-keys/1/regenerate" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Plugins

**List plugins:**
```bash
curl "$CONCIERGE_API_URL/plugins" \
  -H "Authorization: Bearer $TOKEN"
```

**Get dashboard data:**
```bash
curl "$CONCIERGE_API_URL/plugins/dashboard" \
  -H "Authorization: Bearer $TOKEN"
```

**Reload plugin:**
```bash
curl -X POST "$CONCIERGE_API_URL/plugins/news/reload" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Query Parameters

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | Page number (default: 1) |
| `per_page` | int | Items per page (default: 20) |

### Filter Parameters

| Endpoint | Parameter | Description |
|----------|-----------|-------------|
| `/concerts` | `city` | Filter by city |
| `/concerts` | `venue` | Filter by venue |
| `/concerts` | `upcoming` | Future concerts only |
| `/events` | `city` | Filter by city |
| `/events` | `category` | Filter by category |
| `/events` | `upcoming` | Future events only |
| `/news` | `category` | Filter by category |
| `/news` | `confirmed` | Filter by verification status |
| `/news` | `unsent` | Unsent items only |
| `/careers/jobs` | `company` | Filter by company |
| `/careers/jobs` | `location` | Filter by location |
| `/careers/jobs` | `remote` | Remote jobs only |
| `/careers/jobs` | `site` | Filter by job site |
| `/careers/jobs` | `unsent` | Unsent items only |
| `/careers/jobs` | `search` | Search title/company |

---

## Response Format

All list endpoints return:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5,
  "layout": {
    "title_field": "title",
    "title_link_field": "source_url",
    "subtitle_fields": [...],
    "body_fields": [...],
    "icon": "Music",
    "color": "purple"
  }
}
```

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Bad request / validation error |
| 401 | Invalid or missing authentication |
| 403 | Admin access required |
| 404 | Resource not found |
| 500 | Internal server error |
