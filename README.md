# OpenClaw Concierge Dashboard

A dashboard for browsing and managing data collected by your OpenClaw AI instance. Track concerts, events, news, and career opportunities all in one place.

## Features

- **Concerts**: Browse upcoming concerts and shows
- **Events**: Local events and exhibitions
- **News**: News articles with drip-feed functionality
- **Career**: Job listings and company research with markdown rendering

## Tech Stack

- **Backend**: Flask + SQLAlchemy + SQLite
- **Frontend**: React + Vite + TailwindCSS
- **Authentication**: JWT tokens for dashboard, API keys for OpenClaw integration

## Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies (using uv):
   ```bash
   uv sync
   ```

3. Copy the environment file and configure:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your own secret keys.

4. Create the admin user:
   ```bash
   uv run python setup_admin.py
   ```

5. Run the server:
   ```bash
   uv run flask run
   ```
   The API will be available at `http://localhost:5000`

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   The dashboard will be available at `http://localhost:3000`

## API Documentation

See [backend/API.md](backend/API.md) for complete API documentation.

## Configuration

### Environment Variables (Backend)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `JWT_SECRET_KEY` | Secret key for JWT token signing |
| `API_KEY` | API key for OpenClaw integration |
| `DATABASE_URL` | SQLite database URL (default: `sqlite:///concierge.db`) |

## OpenClaw Integration

To add data from your OpenClaw AI instance, use the API endpoints with the `X-API-Key` header:

```bash
curl -X POST http://localhost:5000/api/news \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"title": "Article Title", "category": "Tech", "summary": "..."}'
```

### News Drip Feed

To pop the next unsent news article (marks it as sent):

```bash
curl -X POST http://localhost:5000/api/news/pop \
  -H "X-API-Key: your-api-key"
```
