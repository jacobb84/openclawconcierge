---
name: concierge
description: Add concerts, events, news articles, job listings, and company research to the user's personal Concierge dashboard. Use when user finds interesting content they want to track or review later.
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      env: ["CONCIERGE_API_URL", "CONCIERGE_API_KEY"]
---

# Concierge Dashboard CLI

Add items to the user's personal Concierge dashboard for later review. The dashboard tracks concerts, local events, news, job opportunities, and company research.

## Setup

Set environment variables:
- `CONCIERGE_API_URL`: Base URL for the API (e.g., `http://localhost:5000/api`)
- `CONCIERGE_API_KEY`: API key for authentication

## Commands

### Concerts

**Add a concert:**
```bash
python concierge-cli.py concerts add \
  --artists "Artist 1" \
  --artists "Artist 2" \
  --date 2026-09-25 \
  --venue "Venue Name" \
  --city "Worcester, MA" \
  --url "https://tickets.example.com"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--artists` | Yes | Artist name (can be repeated for multiple) |
| `--date` | Yes | Concert date (YYYY-MM-DD) |
| `--venue` | Yes | Venue name |
| `--city` | Yes | City and state |
| `--url` | No | Ticket or source URL |

**Prune past concerts:**
```bash
python concierge-cli.py concerts prune
```

### Events

**Add an event:**
```bash
python concierge-cli.py events add \
  --title "Event Title" \
  --date 2026-09-25 \
  --city "Boston, MA" \
  --category "exhibition" \
  --summary "Brief description" \
  --url "https://event.example.com"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--title` | Yes | Event title |
| `--date` | Yes | Event date (YYYY-MM-DD) |
| `--city` | Yes | City and state |
| `--category` | No | Category (exhibition, festival, workshop, sports, theater, music, food, community) |
| `--summary` | No | Brief description |
| `--url` | No | Event URL |

**Prune past events:**
```bash
python concierge-cli.py events prune
```

### News

**Add a news article:**
```bash
python concierge-cli.py news add \
  --title "Article Title" \
  --date 2026-03-16 \
  --category "AI & Tech" \
  --summary "Brief summary of the article" \
  --url "https://news.example.com/article" \
  --tags "ai" \
  --tags "technology"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--title` | Yes | Article title |
| `--date` | No | Publication date (YYYY-MM-DD, defaults to today) |
| `--category` | No | News category |
| `--summary` | No | Article summary |
| `--url` | No | Source URL |
| `--tags` | No | Tags (can be repeated) |
| `--confirmed` | No | Mark as fact-checked |

**Pop next news article (drip feed):**
```bash
python concierge-cli.py news pop
```

Gets the oldest unsent article and marks it as sent.

**Prune news (mark all as sent):**
```bash
python concierge-cli.py news prune
```

### Careers

**Add a job listing:**
```bash
python concierge-cli.py careers add-job \
  --title "Senior Software Engineer" \
  --company "Acme Corp" \
  --location "Boston, MA" \
  --salary-min 150000 \
  --salary-max 200000 \
  --url "https://jobs.example.com/12345" \
  --site "linkedin" \
  --remote \
  --summary "Brief summary"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--title` | Yes | Job title |
| `--company` | Yes | Company name |
| `--location` | No | Job location |
| `--salary-min` | No | Minimum salary |
| `--salary-max` | No | Maximum salary |
| `--url` | No | Job listing URL |
| `--site` | No | Job site (linkedin, indeed, etc.) |
| `--remote` | No | Flag for remote position |
| `--summary` | No | Job summary |

**Add company research:**
```bash
python concierge-cli.py careers add-company \
  --name "Company Name" \
  --location "San Francisco, CA" \
  --url "https://company.example.com" \
  --research "# Company Research\n\nMarkdown notes..."
```

| Option | Required | Description |
|--------|----------|-------------|
| `--name` | Yes | Company name |
| `--location` | No | Company location |
| `--url` | No | Company website |
| `--research` | No | Markdown research notes |

## Usage Examples

**User: "Add this concert to my dashboard"**
```bash
python concierge-cli.py concerts add \
  --artists "Kamelot" \
  --artists "Visions of Atlantis" \
  --date 2026-09-25 \
  --venue "The Palladium" \
  --city "Worcester, MA"
```

**User: "Save this job listing"**
```bash
python concierge-cli.py careers add-job \
  --title "Staff Engineer" \
  --company "TechCorp" \
  --location "Remote" \
  --remote \
  --salary-min 180000 \
  --salary-max 220000
```

**User: "Add this news article"**
```bash
python concierge-cli.py news add \
  --title "New AI Breakthrough" \
  --category "AI & Tech" \
  --summary "Researchers announce major advancement..." \
  --url "https://news.example.com/ai-breakthrough"
```

**User: "Research this company for me"**
```bash
python concierge-cli.py careers add-company \
  --name "Acme Corp" \
  --location "Boston, MA" \
  --url "https://acme.com" \
  --research "# Acme Corp\n\n## Overview\n\nAcme Corp is a leading..."
```

**User: "Clean up old concerts"**
```bash
python concierge-cli.py concerts prune
```

**User: "Get me the next news article to share"**
```bash
python concierge-cli.py news pop
```
