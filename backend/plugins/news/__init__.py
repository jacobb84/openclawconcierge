from datetime import date, datetime
from typing import List, Optional, Dict, Any, Type
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, JSON, DateTime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import Base, get_db
from core.models import User
from core.security import get_current_user, verify_api_key
from core.plugin_base import BasePlugin, CardLayout, CardField, PluginConfig


class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    category = Column(String(100), nullable=True)
    date = Column(Date, nullable=True)
    sent = Column(Date, nullable=True)
    summary = Column(Text, nullable=True)
    source_url = Column(String(1000), nullable=True)
    confirmed = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, for_dashboard: bool = False):
        result = {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "date": self.date.isoformat() if self.date else None,
            "summary": self.summary,
            "source_url": self.source_url,
            "confirmed": self.confirmed,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if not for_dashboard:
            result["sent"] = self.sent.isoformat() if self.sent else None
        return result


class NewsCreate(BaseModel):
    title: str
    category: Optional[str] = None
    date: str
    sent: Optional[str] = None
    summary: str
    source_url: str
    confirmed: bool = False
    tags: Optional[List[str]] = None
    
    @classmethod
    def validate_required(cls, data: dict) -> List[str]:
        errors = []
        if not data.get('title'):
            errors.append('Title is required')
        if not data.get('summary'):
            errors.append('Summary is required')
        if not data.get('date'):
            errors.append('Date is required')
        if not data.get('source_url'):
            errors.append('Source URL is required')
        return errors


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    sent: Optional[str] = None
    summary: Optional[str] = None
    source_url: Optional[str] = None
    confirmed: Optional[bool] = None
    tags: Optional[List[str]] = None


def parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


class Plugin(BasePlugin):
    name = "news"
    display_name = "News"
    description = "News articles and updates"
    version = "1.0.0"
    
    def get_models(self) -> List[Type]:
        return [News]
    
    def get_card_layout(self) -> CardLayout:
        return CardLayout(
            title_field="title",
            title_link_field="source_url",
            subtitle_fields=[
                CardField(key="date", label="Date", type="date", icon="Calendar"),
                CardField(key="category", label="Category", type="badge", class_name="badge-blue"),
            ],
            body_fields=[
                CardField(key="summary", label="Summary", type="text"),
                CardField(key="tags", label="Tags", type="tags", class_name="badge-gray"),
            ],
            badge_field=CardField(
                key="confirmed",
                label="Status",
                type="badge",
                class_name="badge-green|badge-yellow"
            ),
            icon="Newspaper",
            color="green"
        )
    
    def get_dashboard_query(self, db: Session, limit: int = 3) -> Dict[str, Any]:
        query = db.query(News).filter(News.sent.is_(None)).order_by(News.date.desc())
        total = query.count()
        items = query.limit(limit).all()
        return {
            "items": [item.to_dict(for_dashboard=True) for item in items],
            "total": total
        }
    
    def get_router(self) -> APIRouter:
        router = APIRouter()
        
        @router.get("")
        def get_news(
            page: int = Query(1, ge=1),
            per_page: int = Query(20, ge=1, le=100),
            category: Optional[str] = None,
            confirmed: Optional[str] = None,
            unsent: Optional[str] = None,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            query = db.query(News).order_by(News.date.desc())
            
            if category:
                query = query.filter(News.category.ilike(f"%{category}%"))
            if confirmed == "true":
                query = query.filter(News.confirmed == True)
            elif confirmed == "false":
                query = query.filter(News.confirmed == False)
            if unsent == "true":
                query = query.filter(News.sent.is_(None))
            
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
        
        @router.get("/{news_id}")
        def get_news_item(
            news_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(News).filter(News.id == news_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="News not found")
            return item.to_dict()
        
        @router.post("", status_code=201)
        def create_news(
            data: NewsCreate,
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            errors = NewsCreate.validate_required(data.model_dump())
            if errors:
                raise HTTPException(status_code=422, detail={'validation_errors': errors})
            
            item = News(
                title=data.title,
                category=data.category,
                date=parse_date(data.date),
                sent=parse_date(data.sent),
                summary=data.summary,
                source_url=data.source_url,
                confirmed=data.confirmed,
                tags=data.tags
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.put("/{news_id}")
        def update_news(
            news_id: int,
            data: NewsUpdate,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(News).filter(News.id == news_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="News not found")
            
            if data.title is not None:
                item.title = data.title
            if data.category is not None:
                item.category = data.category
            if data.date is not None:
                item.date = parse_date(data.date)
            if data.sent is not None:
                item.sent = parse_date(data.sent)
            if data.summary is not None:
                item.summary = data.summary
            if data.source_url is not None:
                item.source_url = data.source_url
            if data.confirmed is not None:
                item.confirmed = data.confirmed
            if data.tags is not None:
                item.tags = data.tags
            
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.delete("/{news_id}")
        def delete_news(
            news_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(News).filter(News.id == news_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="News not found")
            db.delete(item)
            db.commit()
            return {"message": "News deleted"}
        
        @router.post("/pop")
        def pop_news(
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            """Get one unsent news article and mark it as sent."""
            item = db.query(News).filter(News.sent.is_(None)).order_by(News.date.asc()).first()
            if not item:
                raise HTTPException(status_code=204, detail="No unsent news available")
            
            item.sent = date.today()
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.post("/prune")
        def prune_news(
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            """Mark all unsent news as sent."""
            today = date.today()
            count = db.query(News).filter(News.sent.is_(None)).update({"sent": today})
            db.commit()
            return {"message": f"Marked {count} news items as sent"}
        
        return router
