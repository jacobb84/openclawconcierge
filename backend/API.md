# OpenClaw Concierge API Documentation

Base URL: `http://localhost:5000/api`

## Overview

The OpenClaw Concierge API is a plugin-based system built on FastAPI. Each feature (concerts, events, news, careers) is implemented as a plugin that provides its own routes, database models, and card layout definitions.

## Authentication

### Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access_token": "jwt-token-string",
  "user": {
    "id": 1,
    "username": "admin",
    "is_admin": true,
    "created_at": "2026-03-16T12:00:00"
  }
}
```

### Get Current User
**GET** `/auth/me`

**Headers:** `Authorization: Bearer <token>`

---

## Authorization

Two authentication methods are supported:

1. **JWT Token** (for dashboard users): Include `Authorization: Bearer <token>` header
2. **API Key** (for OpenClaw integration): Include `X-API-Key: <api-key>` header

| Endpoint Type | JWT | API Key |
|---------------|-----|---------|
| GET (read)    | ✓   | ✗       |
| POST (create) | ✗   | ✓       |
| PUT (update)  | ✓   | ✗       |
| DELETE        | ✓   | ✗       |
| POST /prune   | ✗   | ✓       |
| POST /pop     | ✗   | ✓       |

---

## Plugins

### List Plugins
**GET** `/plugins`

**Headers:** `Authorization: Bearer <token>`

Returns metadata about all loaded plugins including their card layouts.

### Get Dashboard Data
**GET** `/plugins/dashboard`

**Headers:** `Authorization: Bearer <token>`

Returns dashboard data from all plugins with items sorted appropriately (future items for concerts/events, unsent for news/jobs).

---

## API Keys Management

Full CRUD operations for API keys (admin only).

### List API Keys
**GET** `/api-keys`

### Create API Key
**POST** `/api-keys`

**Request Body:**
```json
{
  "name": "My API Key"
}
```

### Update API Key
**PUT** `/api-keys/<id>`

**Request Body:**
```json
{
  "name": "Updated Name",
  "is_active": true
}
```

### Delete API Key
**DELETE** `/api-keys/<id>`

### Regenerate API Key
**POST** `/api-keys/<id>/regenerate`

---

## Concerts Plugin

### List Concerts
**GET** `/concerts`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| city | string | Filter by city |
| venue | string | Filter by venue |
| upcoming | boolean | Filter to future concerts only |

**Response includes:** `items`, `total`, `page`, `per_page`, `pages`, `layout`

### Create Concert
**POST** `/concerts`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "artists": ["Artist 1", "Artist 2"],
  "date": "2026-09-25",
  "venue": "Venue Name",
  "city": "City, State",
  "source_url": "https://..."
}
```

### Update Concert
**PUT** `/concerts/<id>`

### Delete Concert
**DELETE** `/concerts/<id>`

### Prune Past Concerts
**POST** `/concerts/prune`

**Headers:** `X-API-Key: <api-key>`

Deletes all concerts with dates in the past.

---

## Events Plugin

### List Events
**GET** `/events`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| city | string | Filter by city |
| category | string | Filter by category |
| upcoming | boolean | Filter to future events only |

### Create Event
**POST** `/events`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "title": "Event Title",
  "category": "exhibition",
  "summary": "Description...",
  "date": "2026-09-25",
  "city": "City, State",
  "source_url": "https://..."
}
```

### Update Event
**PUT** `/events/<id>`

### Delete Event
**DELETE** `/events/<id>`

### Prune Past Events
**POST** `/events/prune`

**Headers:** `X-API-Key: <api-key>`

Deletes all events with dates in the past.

---

## News Plugin

### List News
**GET** `/news`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| category | string | Filter by category |
| confirmed | boolean | Filter by verification status |
| unsent | boolean | Filter to unsent items only |

### Create News
**POST** `/news`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "title": "News Title",
  "category": "AI & Tech",
  "date": "2026-03-16",
  "summary": "Summary...",
  "source_url": "https://...",
  "confirmed": false,
  "tags": ["ai", "tech"]
}
```

### Pop News (Drip Feed)
**POST** `/news/pop`

**Headers:** `X-API-Key: <api-key>`

Gets the oldest unsent news article and marks it as sent.

### Prune News
**POST** `/news/prune`

**Headers:** `X-API-Key: <api-key>`

Marks all unsent news as sent.

### Update News
**PUT** `/news/<id>`

### Delete News
**DELETE** `/news/<id>`

---

## Careers Plugin

### Jobs

#### List Jobs
**GET** `/careers/jobs`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| company | string | Filter by company |
| location | string | Filter by location |
| remote | boolean | Filter remote jobs only |
| site | string | Filter by job site |
| unsent | boolean | Filter to unsent items only |
| search | string | Search by title or company |

#### Create Job
**POST** `/careers/jobs`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "title": "Senior Software Engineer",
  "company": "Acme Corp",
  "location": "Boston, MA",
  "salary_min": 150000,
  "salary_max": 200000,
  "job_url": "https://...",
  "site": "linkedin",
  "date_posted": "2026-03-16",
  "is_remote": true,
  "summary": "Brief summary"
}
```

#### Pop Job
**POST** `/careers/jobs/pop`

**Headers:** `X-API-Key: <api-key>`

Gets the oldest unsent job and marks it as sent.

### Companies

#### List Companies
**GET** `/careers/companies`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| location | string | Filter by location |
| search | string | Search by company name |
| include_research | boolean | Include research markdown |

#### Create Company
**POST** `/careers/companies`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "title": "Company Name",
  "location": "San Francisco, CA",
  "url": "https://company.com",
  "research_date": "2026-03-16",
  "research": "# Company Research\n\nMarkdown notes..."
}
```

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
| 401 | Invalid or missing authentication |
| 403 | Admin access required |
| 404 | Resource not found |
| 400 | Bad request / validation error |
| 500 | Internal server error |
