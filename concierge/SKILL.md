---
name: concierge
description: Add concerts, events, news articles, job listings, and company research to the user's personal Concierge dashboard. Use when user finds interesting content they want to track or review later.
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      env: ["CONCIERGE_API_URL", "CONCIERGE_API_KEY"]
---

# Concierge Dashboard API

Add items to the user's personal Concierge dashboard for later review. The dashboard tracks concerts, local events, news, job opportunities, and company research.

## Setup

Set environment variables:
- `CONCIERGE_API_URL`: Base URL for the API (e.g., `https://api.example.com/api`)
- `CONCIERGE_API_KEY`: API key for authentication

## API Endpoints

All POST requests require the `X-API-Key` header.

### Add Concert

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

**Required fields:** `artists`, `date`, `venue`, `city`
**Optional fields:** `source_url`

### Add Event

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

**Required fields:** `title`, `date`, `city`
**Optional fields:** `category`, `summary`, `source_url`

**Categories:** exhibition, festival, workshop, sports, theater, music, food, community

### Add News

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

**Required fields:** `title`, `date`
**Optional fields:** `category`, `summary`, `source_url`, `confirmed`, `tags`

### Add Job

```bash
curl -X POST "$CONCIERGE_API_URL/career/jobs" \
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
    "description": "Full job description...",
    "summary": "Brief summary"
  }'
```

**Required fields:** `title`, `company`
**Optional fields:** `location`, `salary_min`, `salary_max`, `job_url`, `site`, `date_posted`, `is_remote`, `description`, `summary`

### Add Company Research

```bash
curl -X POST "$CONCIERGE_API_URL/career/companies" \
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

**Required fields:** `title`
**Optional fields:** `location`, `url`, `research_date`, `research`

### Pop News (Drip Feed)

Get the next unsent news article and mark it as sent:

```bash
curl -X POST "$CONCIERGE_API_URL/news/pop" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

Returns the news article or 204 if no unsent articles available.

## Usage Examples

**User: "Add this concert to my dashboard"**
```bash
curl -X POST "$CONCIERGE_API_URL/concerts" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{"artists": ["Kamelot", "Visions of Atlantis"], "date": "2026-09-25", "venue": "The Palladium", "city": "Worcester, MA"}'
```

**User: "Save this job listing"**
```bash
curl -X POST "$CONCIERGE_API_URL/career/jobs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{"title": "Staff Engineer", "company": "TechCorp", "location": "Remote", "is_remote": true, "salary_min": 180000, "salary_max": 220000}'
```

**User: "Add this news article"**
```bash
curl -X POST "$CONCIERGE_API_URL/news" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{"title": "New AI Breakthrough", "date": "2026-03-16", "category": "AI & Tech", "summary": "Researchers announce...", "source_url": "https://..."}'
```

**User: "Research this company for me"**
```bash
curl -X POST "$CONCIERGE_API_URL/career/companies" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{"title": "Acme Corp", "location": "Boston, MA", "url": "https://acme.com", "research": "# Acme Corp\n\n## Overview\n\nAcme Corp is a..."}'
```

## Response Format

All successful POST requests return the created object with an `id` field:

```json
{
  "id": 1,
  "title": "...",
  "created_at": "2026-03-16T12:00:00",
  ...
}
```

## Error Responses

- `401`: Invalid or missing API key
- `400`: Missing required fields
- `500`: Server error
