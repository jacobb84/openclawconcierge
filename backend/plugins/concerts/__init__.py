from datetime import date, datetime
from typing import List, Optional, Dict, Any, Type
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import Column, Integer, String, Date, JSON, DateTime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import Base, get_db
from core.models import User
from core.security import get_current_user, verify_api_key
from core.plugin_base import BasePlugin, CardLayout, CardField, PluginConfig


class Concert(Base):
    __tablename__ = "concerts"
    
    id = Column(Integer, primary_key=True, index=True)
    artists = Column(JSON, nullable=False)
    date = Column(Date, nullable=True)
    venue = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, for_dashboard: bool = False):
        return {
            "id": self.id,
            "artists": self.artists,
            "title": ", ".join(self.artists) if self.artists else "Unknown Artists",
            "date": self.date.isoformat() if self.date else None,
            "venue": self.venue,
            "city": self.city,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ConcertCreate(BaseModel):
    artists: List[str]
    date: Optional[str] = None
    venue: Optional[str] = None
    city: Optional[str] = None
    source_url: Optional[str] = None


class ConcertUpdate(BaseModel):
    artists: Optional[List[str]] = None
    date: Optional[str] = None
    venue: Optional[str] = None
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
    name = "concerts"
    display_name = "Concerts"
    description = "Upcoming concerts and shows"
    version = "1.0.0"
    
    def get_models(self) -> List[Type]:
        return [Concert]
    
    def get_card_layout(self) -> CardLayout:
        return CardLayout(
            title_field="title",
            title_link_field="source_url",
            subtitle_fields=[
                CardField(key="date", label="Date", type="date", icon="Calendar"),
                CardField(key="venue", label="Venue", type="text", icon="Music"),
            ],
            body_fields=[
                CardField(key="city", label="Location", type="text", icon="MapPin"),
            ],
            icon="Music",
            color="purple"
        )
    
    def get_dashboard_query(self, db: Session, limit: int = 3) -> Dict[str, Any]:
        today = date.today()
        query = db.query(Concert).filter(
            (Concert.date >= today) | (Concert.date.is_(None))
        ).order_by(Concert.date.asc())
        total = query.count()
        items = query.limit(limit).all()
        return {
            "items": [item.to_dict(for_dashboard=True) for item in items],
            "total": total
        }
    
    def get_router(self) -> APIRouter:
        router = APIRouter()
        
        @router.get("")
        def get_concerts(
            page: int = Query(1, ge=1),
            per_page: int = Query(20, ge=1, le=100),
            city: Optional[str] = None,
            venue: Optional[str] = None,
            upcoming: Optional[str] = None,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            query = db.query(Concert).order_by(Concert.date.desc())
            
            if city:
                query = query.filter(Concert.city.ilike(f"%{city}%"))
            if venue:
                query = query.filter(Concert.venue.ilike(f"%{venue}%"))
            if upcoming == "true":
                today = date.today()
                query = query.filter(
                    (Concert.date >= today) | (Concert.date.is_(None))
                ).order_by(Concert.date.asc())
            
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
        
        @router.get("/{concert_id}")
        def get_concert(
            concert_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Concert).filter(Concert.id == concert_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Concert not found")
            return item.to_dict()
        
        @router.post("", status_code=201)
        def create_concert(
            data: ConcertCreate,
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            item = Concert(
                artists=data.artists,
                date=parse_date(data.date),
                venue=data.venue,
                city=data.city,
                source_url=data.source_url
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.put("/{concert_id}")
        def update_concert(
            concert_id: int,
            data: ConcertUpdate,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Concert).filter(Concert.id == concert_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Concert not found")
            
            if data.artists is not None:
                item.artists = data.artists
            if data.date is not None:
                item.date = parse_date(data.date)
            if data.venue is not None:
                item.venue = data.venue
            if data.city is not None:
                item.city = data.city
            if data.source_url is not None:
                item.source_url = data.source_url
            
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.delete("/{concert_id}")
        def delete_concert(
            concert_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Concert).filter(Concert.id == concert_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Concert not found")
            db.delete(item)
            db.commit()
            return {"message": "Concert deleted"}
        
        @router.post("/prune")
        def prune_concerts(
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            """Delete all concerts that have already happened."""
            today = date.today()
            count = db.query(Concert).filter(Concert.date < today).delete()
            db.commit()
            return {"message": f"Deleted {count} past concerts"}
        
        return router
