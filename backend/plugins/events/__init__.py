from datetime import date, datetime
from typing import List, Optional, Dict, Any, Type
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import Base, get_db
from core.models import User
from core.security import get_current_user, verify_api_key
from core.plugin_base import BasePlugin, CardLayout, CardField, PluginConfig


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    category = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    date = Column(Date, nullable=True)
    city = Column(String(100), nullable=True)
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, for_dashboard: bool = False):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "summary": self.summary,
            "date": self.date.isoformat() if self.date else None,
            "city": self.city,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class EventCreate(BaseModel):
    title: str
    category: str
    summary: str
    date: str
    city: str
    source_url: Optional[str] = None
    
    @classmethod
    def validate_required(cls, data: dict) -> List[str]:
        errors = []
        if not data.get('title'):
            errors.append('Title is required')
        if not data.get('category'):
            errors.append('Category is required')
        if not data.get('summary'):
            errors.append('Summary is required')
        if not data.get('date'):
            errors.append('Date is required')
        if not data.get('city'):
            errors.append('City/location is required')
        return errors


class EventUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    date: Optional[str] = None
    city: Optional[str] = None
    source_url: Optional[str] = None


def parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


class Plugin(BasePlugin):
    name = "events"
    display_name = "Events"
    description = "Local events and exhibitions"
    version = "1.0.0"
    
    def get_models(self) -> List[Type]:
        return [Event]
    
    def get_card_layout(self) -> CardLayout:
        return CardLayout(
            title_field="title",
            title_link_field="source_url",
            subtitle_fields=[
                CardField(key="date", label="Date", type="date", icon="Calendar"),
                CardField(key="category", label="Category", type="badge", class_name="badge-blue"),
            ],
            body_fields=[
                CardField(key="city", label="Location", type="text", icon="MapPin"),
                CardField(key="summary", label="Summary", type="text"),
            ],
            icon="Calendar",
            color="blue"
        )
    
    def get_dashboard_query(self, db: Session, limit: int = 3) -> Dict[str, Any]:
        today = date.today()
        query = db.query(Event).filter(
            (Event.date >= today) | (Event.date.is_(None))
        ).order_by(Event.date.asc())
        total = query.count()
        items = query.limit(limit).all()
        return {
            "items": [item.to_dict(for_dashboard=True) for item in items],
            "total": total
        }
    
    def get_router(self) -> APIRouter:
        router = APIRouter()
        
        @router.get("")
        def get_events(
            page: int = Query(1, ge=1),
            per_page: int = Query(20, ge=1, le=100),
            city: Optional[str] = None,
            category: Optional[str] = None,
            upcoming: Optional[str] = None,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            query = db.query(Event).order_by(Event.date.desc())
            
            if city:
                query = query.filter(Event.city.ilike(f"%{city}%"))
            if category:
                query = query.filter(Event.category.ilike(f"%{category}%"))
            if upcoming == "true":
                today = date.today()
                query = query.filter(
                    (Event.date >= today) | (Event.date.is_(None))
                ).order_by(Event.date.asc())
            
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
        
        @router.get("/{event_id}")
        def get_event(
            event_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Event).filter(Event.id == event_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Event not found")
            return item.to_dict()
        
        @router.post("", status_code=201)
        def create_event(
            data: EventCreate,
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            errors = EventCreate.validate_required(data.model_dump())
            if errors:
                raise HTTPException(status_code=422, detail={'validation_errors': errors})
            
            item = Event(
                title=data.title,
                category=data.category,
                summary=data.summary,
                date=parse_date(data.date),
                city=data.city,
                source_url=data.source_url
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.put("/{event_id}")
        def update_event(
            event_id: int,
            data: EventUpdate,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Event).filter(Event.id == event_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Event not found")
            
            if data.title is not None:
                item.title = data.title
            if data.category is not None:
                item.category = data.category
            if data.summary is not None:
                item.summary = data.summary
            if data.date is not None:
                item.date = parse_date(data.date)
            if data.city is not None:
                item.city = data.city
            if data.source_url is not None:
                item.source_url = data.source_url
            
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.delete("/{event_id}")
        def delete_event(
            event_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Event).filter(Event.id == event_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Event not found")
            db.delete(item)
            db.commit()
            return {"message": "Event deleted"}
        
        @router.post("/prune")
        def prune_events(
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            """Delete all events that have already happened."""
            today = date.today()
            count = db.query(Event).filter(Event.date < today).delete()
            db.commit()
            return {"message": f"Deleted {count} past events"}
        
        return router
