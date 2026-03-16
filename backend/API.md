# OpenClaw Concierge API Documentation

Base URL: `http://localhost:5000/api`

## Authentication

### Login
**POST** `/auth/login`

Authenticate a user and receive a JWT token.

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

**Response (200):**
```json
{
  "id": 1,
  "username": "admin",
  "is_admin": true,
  "created_at": "2026-03-16T12:00:00"
}
```

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

---

## Concerts

### List Concerts
**GET** `/concerts`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| city | string | Filter by city (partial match) |
| venue | string | Filter by venue (partial match) |
| unsent | boolean | Filter to only unsent items |

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "artists": ["Kamelot", "Visions of Atlantis"],
      "date": "2026-09-25",
      "venue": "The Palladium",
      "city": "Worcester, MA",
      "source_url": "https://...",
      "sent": "2026-03-11",
      "created_at": "2026-03-16T12:00:00",
      "updated_at": "2026-03-16T12:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Get Concert
**GET** `/concerts/<id>`

**Headers:** `Authorization: Bearer <token>`

**Response (200):** Single concert object

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
  "source_url": "https://...",
  "sent": null
}
```

**Response (201):** Created concert object

### Update Concert
**PUT** `/concerts/<id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:** Partial concert object (only include fields to update)

**Response (200):** Updated concert object

### Delete Concert
**DELETE** `/concerts/<id>`

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{ "message": "Concert deleted" }
```

---

## Events

### List Events
**GET** `/events`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| city | string | Filter by city (partial match) |
| category | string | Filter by category (partial match) |
| unsent | boolean | Filter to only unsent items |

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Event Title",
      "category": "exhibition",
      "summary": "Event description...",
      "date": "2026-09-25",
      "city": "Worcester, MA",
      "source_url": "https://...",
      "sent": "2026-03-11",
      "created_at": "2026-03-16T12:00:00",
      "updated_at": "2026-03-16T12:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Get Event
**GET** `/events/<id>`

**Headers:** `Authorization: Bearer <token>`

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
  "source_url": "https://...",
  "sent": null
}
```

### Update Event
**PUT** `/events/<id>`

**Headers:** `Authorization: Bearer <token>`

### Delete Event
**DELETE** `/events/<id>`

**Headers:** `Authorization: Bearer <token>`

---

## News

### List News
**GET** `/news`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| category | string | Filter by category (partial match) |
| confirmed | boolean | Filter by confirmed status |
| unsent | boolean | Filter to only unsent items |

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "News Title",
      "category": "AI & Tech",
      "date": "2026-03-16",
      "sent": "2026-03-16",
      "summary": "Summary...",
      "source_url": "https://...",
      "confirmed": true,
      "tags": ["ai", "tech"],
      "created_at": "2026-03-16T12:00:00",
      "updated_at": "2026-03-16T12:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Pop News (Drip Feed)
**POST** `/news/pop`

**Headers:** `X-API-Key: <api-key>`

Retrieves the oldest unsent news article and marks it as sent with today's date.

**Response (200):** Single news object with updated `sent` field

**Response (204):** No unsent news available

### Get News Item
**GET** `/news/<id>`

**Headers:** `Authorization: Bearer <token>`

### Create News
**POST** `/news`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "title": "News Title",
  "category": "AI & Tech",
  "date": "2026-03-16",
  "sent": null,
  "summary": "Summary...",
  "source_url": "https://...",
  "confirmed": false,
  "tags": ["ai", "tech"]
}
```

### Update News
**PUT** `/news/<id>`

**Headers:** `Authorization: Bearer <token>`

### Delete News
**DELETE** `/news/<id>`

**Headers:** `Authorization: Bearer <token>`

---

## Career - Companies

### List Companies
**GET** `/career/companies`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| location | string | Filter by location (partial match) |
| search | string | Search by company name |
| include_research | boolean | Include full research markdown (default: false) |

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Company Name",
      "location": "City, State",
      "research_date": "2026-03-16",
      "url": "https://...",
      "created_at": "2026-03-16T12:00:00",
      "updated_at": "2026-03-16T12:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Get Company
**GET** `/career/companies/<id>`

**Headers:** `Authorization: Bearer <token>`

Returns full company object including `research` markdown field.

### Create Company
**POST** `/career/companies`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "title": "Company Name",
  "location": "City, State",
  "research_date": "2026-03-16",
  "url": "https://...",
  "research": "# Company Research\n\nMarkdown content..."
}
```

### Update Company
**PUT** `/career/companies/<id>`

**Headers:** `Authorization: Bearer <token>`

### Delete Company
**DELETE** `/career/companies/<id>`

**Headers:** `Authorization: Bearer <token>`

---

## Career - Jobs

### List Jobs
**GET** `/career/jobs`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| company | string | Filter by company (partial match) |
| location | string | Filter by location (partial match) |
| remote | boolean | Filter remote jobs only |
| site | string | Filter by job site (e.g., "indeed") |
| unsent | boolean | Filter to only unsent items |
| search | string | Search by title or company |

**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid-string",
      "title": "Job Title",
      "company": "Company Name",
      "company_id": 1,
      "location": "City, State",
      "salary_min": 110000.0,
      "salary_max": 185000.0,
      "job_url": "https://...",
      "site": "indeed",
      "date_posted": "2026-03-16",
      "is_remote": true,
      "description": "Full job description...",
      "summary": "Brief summary...",
      "sent": "2026-03-11",
      "created_at": "2026-03-16T12:00:00",
      "updated_at": "2026-03-16T12:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Get Job
**GET** `/career/jobs/<id>`

**Headers:** `Authorization: Bearer <token>`

### Create Job
**POST** `/career/jobs`

**Headers:** `X-API-Key: <api-key>`

**Request Body:**
```json
{
  "id": "optional-uuid",
  "title": "Job Title",
  "company": "Company Name",
  "company_id": 1,
  "location": "City, State",
  "salary_min": 110000.0,
  "salary_max": 185000.0,
  "job_url": "https://...",
  "site": "indeed",
  "date_posted": "2026-03-16",
  "is_remote": true,
  "description": "Full description...",
  "summary": "Brief summary...",
  "sent": null
}
```

### Update Job
**PUT** `/career/jobs/<id>`

**Headers:** `Authorization: Bearer <token>`

### Delete Job
**DELETE** `/career/jobs/<id>`

**Headers:** `Authorization: Bearer <token>`

---

## Error Responses

All endpoints may return the following error responses:

**401 Unauthorized:**
```json
{ "error": "Invalid or missing API key" }
```
or
```json
{ "msg": "Missing Authorization Header" }
```

**404 Not Found:**
```json
{ "error": "Resource not found" }
```

**400 Bad Request:**
```json
{ "error": "Description of the error" }
```

**500 Internal Server Error:**
```json
{ "error": "Internal server error" }
```
