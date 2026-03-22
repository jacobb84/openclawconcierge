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
- `CONCIERGE_API_URL`: Base URL for the API (e.g., `http://localhost:5000/api`)
- `CONCIERGE_API_KEY`: API key for authentication

## API Endpoints

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

| Field | Required | Description |
|-------|----------|-------------|
| `artists` | **Yes** | Array of artist names (at least one) |
| `date` | **Yes** | Concert date (YYYY-MM-DD) |
| `venue` | **Yes** | Venue name |
| `city` | **Yes** | City and state |
| `source_url` | No | Ticket or source URL |

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
    "category": "exhibition",
    "summary": "Brief description of the event",
    "date": "2026-09-25",
    "city": "Boston, MA",
    "source_url": "https://event.example.com"
  }'
```

| Field | Required | Description |
|-------|----------|-------------|
| `title` | **Yes** | Event title |
| `category` | **Yes** | Category (exhibition, festival, workshop, sports, theater, music, food, community) |
| `summary` | **Yes** | Brief description |
| `date` | **Yes** | Event date (YYYY-MM-DD) |
| `city` | **Yes** | City and state |
| `source_url` | No | Event URL |

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
    "summary": "Brief summary of the article content",
    "source_url": "https://news.example.com/article",
    "category": "AI & Tech",
    "tags": ["ai", "technology"],
    "confirmed": false
  }'
```

| Field | Required | Description |
|-------|----------|-------------|
| `title` | **Yes** | Article title |
| `summary` | **Yes** | Article summary |
| `date` | **Yes** | Publication date (YYYY-MM-DD) |
| `source_url` | **Yes** | Source URL |
| `category` | No | News category |
| `tags` | No | Array of tags |
| `confirmed` | No | Mark as fact-checked (default: false) |

**Pop next news article (drip feed):**
```bash
curl -X POST "$CONCIERGE_API_URL/news/pop" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

Gets the oldest unsent article and marks it as sent.

**Prune news (mark all as sent):**
```bash
curl -X POST "$CONCIERGE_API_URL/news/prune" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

---

### Jobs

**Add a job listing:**
```bash
curl -X POST "$CONCIERGE_API_URL/careers/jobs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Senior Software Engineer",
    "company": "Acme Corp",
    "description": "Full job description text here...",
    "date_posted": "2026-03-16",
    "location": "Boston, MA",
    "salary_min": 150000,
    "salary_max": 200000,
    "job_url": "https://jobs.example.com/12345",
    "site": "linkedin",
    "is_remote": true,
    "summary": "Brief summary"
  }'
```

| Field | Required | Description |
|-------|----------|-------------|
| `title` | **Yes** | Job title |
| `company` | **Yes** | Company name |
| `description` | **Yes** | Full job description |
| `date_posted` | **Yes** | Date posted (YYYY-MM-DD) |
| `location` | No | Job location |
| `salary_min` | No | Minimum salary |
| `salary_max` | No | Maximum salary |
| `job_url` | No | Job listing URL |
| `site` | No | Job site (linkedin, indeed, etc.) |
| `is_remote` | No | Remote position (default: false) |
| `summary` | No | Brief summary |

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
    "research_date": "2026-03-16",
    "url": "https://company.example.com",
    "research": "# Company Research\n\n## Overview\n\nMarkdown notes about the company..."
  }'
```

| Field | Required | Description |
|-------|----------|-------------|
| `title` | **Yes** | Company name |
| `location` | **Yes** | Company location |
| `research_date` | **Yes** | Date research was conducted (YYYY-MM-DD) |
| `research` | **Yes** | Markdown research notes |
| `url` | No | Company website |

---

## Usage Examples

**User: "Add this concert to my dashboard"**
```bash
curl -X POST "$CONCIERGE_API_URL/concerts" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "artists": ["Kamelot", "Visions of Atlantis"],
    "date": "2026-09-25",
    "venue": "The Palladium",
    "city": "Worcester, MA"
  }'
```

**User: "Save this job listing"**
```bash
curl -X POST "$CONCIERGE_API_URL/careers/jobs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Staff Engineer",
    "company": "TechCorp",
    "description": "We are looking for a Staff Engineer to lead...",
    "date_posted": "2026-03-16",
    "location": "Remote",
    "is_remote": true,
    "salary_min": 180000,
    "salary_max": 220000
  }'
```

**User: "Add this news article"**
```bash
curl -X POST "$CONCIERGE_API_URL/news" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "New AI Breakthrough",
    "summary": "Researchers announce major advancement in artificial intelligence...",
    "date": "2026-03-16",
    "source_url": "https://news.example.com/ai-breakthrough",
    "category": "AI & Tech"
  }'
```

**User: "Research this company for me"**
```bash
curl -X POST "$CONCIERGE_API_URL/careers/companies" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CONCIERGE_API_KEY" \
  -d '{
    "title": "Acme Corp",
    "location": "Boston, MA",
    "research_date": "2026-03-16",
    "url": "https://acme.com",
    "research": "# Acme Corp\n\n## Overview\n\nAcme Corp is a leading technology company..."
  }'
```

**User: "Clean up old concerts"**
```bash
curl -X POST "$CONCIERGE_API_URL/concerts/prune" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

**User: "Get me the next news article to share"**
```bash
curl -X POST "$CONCIERGE_API_URL/news/pop" \
  -H "X-API-Key: $CONCIERGE_API_KEY"
```

---

## Creating New Plugins

Plugins are self-contained modules that add new data types and API endpoints to the Concierge dashboard. Each plugin lives in its own directory under `backend/plugins/`.

### Plugin Structure

Create a new directory and `__init__.py` file:

```
backend/plugins/
└── myplugin/
    └── __init__.py
```

### Minimal Plugin Template

```python
from datetime import date, datetime
from typing import List, Optional, Dict, Any, Type
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import Base, get_db
from core.models import User
from core.security import get_current_user, verify_api_key
from core.plugin_base import BasePlugin, CardLayout, CardField


# 1. Define your SQLAlchemy model
class MyItem(Base):
    __tablename__ = "my_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=True)
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, for_dashboard: bool = False):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 2. Define Pydantic models for validation
class MyItemCreate(BaseModel):
    title: str
    description: str
    date: str
    source_url: Optional[str] = None
    
    @classmethod
    def validate_required(cls, data: dict) -> List[str]:
        errors = []
        if not data.get('title'):
            errors.append('Title is required')
        if not data.get('description'):
            errors.append('Description is required')
        if not data.get('date'):
            errors.append('Date is required')
        return errors


class MyItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    source_url: Optional[str] = None


def parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


# 3. Define the Plugin class
class Plugin(BasePlugin):
    name = "myplugin"           # URL prefix: /api/myplugin
    display_name = "My Plugin"  # Shown in UI
    description = "Description of what this plugin tracks"
    version = "1.0.0"
    
    def get_models(self) -> List[Type]:
        """Return all SQLAlchemy models for this plugin."""
        return [MyItem]
    
    def get_card_layout(self) -> CardLayout:
        """Define how cards are rendered in the frontend."""
        return CardLayout(
            title_field="title",
            title_link_field="source_url",  # Makes title clickable
            subtitle_fields=[
                CardField(key="date", label="Date", type="date", icon="Calendar"),
            ],
            body_fields=[
                CardField(key="description", label="Description", type="text"),
            ],
            icon="Box",      # Lucide icon name
            color="blue"     # purple, blue, green, orange, gray
        )
    
    def get_dashboard_query(self, db: Session, limit: int = 3) -> Dict[str, Any]:
        """Return items to show on the dashboard."""
        query = db.query(MyItem).order_by(MyItem.date.desc())
        total = query.count()
        items = query.limit(limit).all()
        return {
            "items": [item.to_dict(for_dashboard=True) for item in items],
            "total": total
        }
    
    def get_router(self) -> APIRouter:
        """Define all API routes for this plugin."""
        router = APIRouter()
        
        @router.get("")
        def get_items(
            page: int = Query(1, ge=1),
            per_page: int = Query(20, ge=1, le=100),
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            query = db.query(MyItem).order_by(MyItem.date.desc())
            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            
            return {
                "items": [item.to_dict() for item in items],
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": (total + per_page - 1) // per_page,
                "layout": self.get_card_layout().model_dump()
            }
        
        @router.get("/{item_id}")
        def get_item(
            item_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(MyItem).filter(MyItem.id == item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item.to_dict()
        
        @router.post("", status_code=201)
        def create_item(
            data: MyItemCreate,
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            errors = MyItemCreate.validate_required(data.model_dump())
            if errors:
                raise HTTPException(status_code=422, detail={'validation_errors': errors})
            
            item = MyItem(
                title=data.title,
                description=data.description,
                date=parse_date(data.date),
                source_url=data.source_url
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.put("/{item_id}")
        def update_item(
            item_id: int,
            data: MyItemUpdate,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(MyItem).filter(MyItem.id == item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            
            if data.title is not None:
                item.title = data.title
            if data.description is not None:
                item.description = data.description
            if data.date is not None:
                item.date = parse_date(data.date)
            if data.source_url is not None:
                item.source_url = data.source_url
            
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.delete("/{item_id}")
        def delete_item(
            item_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(MyItem).filter(MyItem.id == item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            db.delete(item)
            db.commit()
            return {"message": "Item deleted"}
        
        return router
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `__tablename__` | Database table name (must be unique) |
| `Plugin.name` | URL prefix and internal identifier |
| `Plugin.display_name` | Human-readable name for UI |
| `get_models()` | Returns SQLAlchemy models to create tables |
| `get_card_layout()` | Defines frontend card rendering |
| `get_dashboard_query()` | Returns items for dashboard preview |
| `get_router()` | Defines all API endpoints |

### CardLayout Options

```python
CardLayout(
    title_field="title",           # Field to use as card title
    title_link_field="source_url", # Field containing URL (makes title clickable)
    subtitle_fields=[              # Fields shown below title
        CardField(key="date", label="Date", type="date", icon="Calendar"),
        CardField(key="category", label="Category", type="badge", class_name="badge-blue"),
    ],
    body_fields=[                  # Fields shown in card body
        CardField(key="summary", label="Summary", type="text"),
        CardField(key="tags", label="Tags", type="tags", class_name="badge-gray"),
    ],
    badge_field=CardField(         # Optional status badge
        key="is_active",
        label="Status",
        type="badge",
        class_name="badge-green"
    ),
    icon="Box",                    # Lucide icon name
    color="blue"                   # Theme color
)
```

### CardField Types

| Type | Description |
|------|-------------|
| `text` | Plain text |
| `date` | Formatted date |
| `badge` | Colored badge/pill |
| `tags` | Array of badges |
| `link` | Clickable URL |

### Available Icons

Use any icon name from [Lucide Icons](https://lucide.dev/icons/): `Calendar`, `MapPin`, `Music`, `Newspaper`, `Briefcase`, `Building2`, `Tag`, `Globe`, `FileText`, etc.

### Available Colors

`purple`, `blue`, `green`, `orange`, `gray`

### Authentication

- **Read endpoints** (`GET`): Use `current_user: User = Depends(get_current_user)` - requires JWT token
- **Write endpoints** (`POST`, `PUT`, `DELETE` for creation): Use `api_key: str = Depends(verify_api_key)` - requires API key
- **Write endpoints** (for user actions like delete from UI): Use `current_user: User = Depends(get_current_user)`

### Hot Reloading

Plugins are automatically detected and loaded on server start. The plugin manager watches for file changes and can reload plugins without restarting the server.

### Adding Frontend Route (Optional)

If you need a dedicated page for your plugin, add a route in `frontend/src/App.jsx` and create a page component following the pattern in `frontend/src/pages/`.
