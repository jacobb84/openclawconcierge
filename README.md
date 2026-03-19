# OpenClaw Concierge Dashboard

A dashboard for browsing and managing data collected by your OpenClaw AI instance. Track concerts, events, news, and career opportunities all in one place.

## Features

- **Concerts**: Browse upcoming concerts and shows
- **Events**: Local events and exhibitions
- **News**: News articles with drip-feed functionality
- **Career**: Job listings and company research with markdown rendering
- **Plugin System**: Extensible architecture with hot-reload configuration
- **CLI**: Command-line interface for concierge skill integration

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + Vite + TailwindCSS
- **Authentication**: JWT tokens for dashboard, API keys for OpenClaw integration
- **CLI**: Typer + httpx

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
   uv run uvicorn main:app --reload
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
| `SECRET_KEY` | Application secret key |
| `JWT_SECRET_KEY` | Secret key for JWT token signing |
| `DATABASE_URL` | SQLite database URL (default: `sqlite:///concierge.db`) |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) |
| `PLUGINS_DIR` | Directory for plugins (default: `plugins`) |
| `PLUGINS_CONFIG` | Plugin configuration file (default: `plugins/plugins.yaml`) |

### Environment Variables (CLI)

| Variable | Description |
|----------|-------------|
| `CONCIERGE_API_URL` | API base URL (default: `http://localhost:5000/api`) |
| `CONCIERGE_API_KEY` | API key for authentication |

## CLI Usage

The CLI provides commands for managing concierge data:

```bash
# Add a concert
uv run python cli.py concerts add --artists "Artist Name" --date 2026-09-25 --venue "Venue" --city "City"

# Add a news article
uv run python cli.py news add --title "Title" --category "Tech" --summary "Summary..."

# Add a job
uv run python cli.py careers add-job --title "Engineer" --company "Acme" --url "https://..."

# Prune past concerts
uv run python cli.py concerts prune

# Pop next news article (drip feed)
uv run python cli.py news pop
```

Run `uv run python cli.py --help` for full command documentation.

## OpenClaw Integration

To add data from your OpenClaw AI instance, use the API endpoints with the `X-API-Key` header:

```bash
curl -X POST http://localhost:5000/api/news \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"title": "Article Title", "category": "Tech", "summary": "..."}'
```

## Plugin System

Plugins are located in `backend/plugins/` and configured via `plugins/plugins.yaml`. Each plugin provides:

- Database models
- API routes
- Card layout definitions for the dashboard

To create a new plugin, extend `BasePlugin` from `core.plugin_base` and implement the required methods.

Hot-reload is supported - edit `plugins.yaml` to enable/disable plugins without restarting.
