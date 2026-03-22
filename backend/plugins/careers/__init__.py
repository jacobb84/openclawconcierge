from datetime import date, datetime
from typing import List, Optional, Dict, Any, Type
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, Float, DateTime, ForeignKey, or_
from sqlalchemy.orm import Session, relationship
from pydantic import BaseModel
from core.database import Base, get_db
from core.models import User
from core.security import get_current_user, verify_api_key
from core.plugin_base import BasePlugin, CardLayout, CardField, PluginConfig


class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    location = Column(String(200), nullable=True)
    research_date = Column(Date, nullable=True)
    url = Column(String(500), nullable=True)
    research = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    jobs = relationship("Job", back_populates="company_ref")
    
    def to_dict(self, include_research: bool = True):
        result = {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "research_date": self.research_date.isoformat() if self.research_date else None,
            "url": self.url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if include_research:
            result["research"] = self.research
        return result


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(300), nullable=False)
    company = Column(String(300), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    location = Column(String(200), nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    job_url = Column(String(500), nullable=True)
    site = Column(String(50), nullable=True)
    date_posted = Column(Date, nullable=True)
    is_remote = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    sent = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company_ref = relationship("Company", back_populates="jobs")
    
    def to_dict(self, for_dashboard: bool = False):
        result = {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "company_id": self.company_id,
            "location": self.location,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "job_url": self.job_url,
            "site": self.site,
            "date_posted": self.date_posted.isoformat() if self.date_posted else None,
            "is_remote": self.is_remote,
            "description": self.description,
            "summary": self.summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if not for_dashboard:
            result["sent"] = self.sent.isoformat() if self.sent else None
        return result


class CompanyCreate(BaseModel):
    title: str
    location: str
    research_date: str
    url: Optional[str] = None
    research: str
    
    @classmethod
    def validate_required(cls, data: dict) -> List[str]:
        errors = []
        if not data.get('title'):
            errors.append('Company name is required')
        if not data.get('location'):
            errors.append('Location is required')
        if not data.get('research_date'):
            errors.append('Research date is required')
        if not data.get('research'):
            errors.append('Research content is required')
        return errors


class CompanyUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    research_date: Optional[str] = None
    url: Optional[str] = None
    research: Optional[str] = None


class JobCreate(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    company_id: Optional[int] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_url: Optional[str] = None
    site: Optional[str] = None
    date_posted: str
    is_remote: bool = False
    description: str
    summary: Optional[str] = None
    sent: Optional[str] = None
    
    @classmethod
    def validate_required(cls, data: dict) -> List[str]:
        errors = []
        if not data.get('title'):
            errors.append('Job title is required')
        if not data.get('company'):
            errors.append('Company name is required')
        if not data.get('description'):
            errors.append('Job description is required')
        if not data.get('date_posted'):
            errors.append('Date posted is required')
        return errors


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_id: Optional[int] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_url: Optional[str] = None
    site: Optional[str] = None
    date_posted: Optional[str] = None
    is_remote: Optional[bool] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    sent: Optional[str] = None


def parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


class Plugin(BasePlugin):
    name = "careers"
    display_name = "Career"
    description = "Job listings and company research"
    version = "1.0.0"
    
    def get_models(self) -> List[Type]:
        return [Company, Job]
    
    def get_card_layout(self) -> CardLayout:
        return CardLayout(
            title_field="title",
            title_link_field="job_url",
            subtitle_fields=[
                CardField(key="company", label="Company", type="text", icon="Building2"),
                CardField(key="location", label="Location", type="text", icon="MapPin"),
            ],
            body_fields=[
                CardField(key="salary_range", label="Salary", type="text", icon="DollarSign"),
                CardField(key="date_posted", label="Posted", type="date", icon="Calendar"),
                CardField(key="summary", label="Summary", type="text"),
            ],
            badge_field=CardField(key="is_remote", label="Remote", type="badge", class_name="badge-green"),
            icon="Briefcase",
            color="orange"
        )
    
    def get_dashboard_query(self, db: Session, limit: int = 3) -> Dict[str, Any]:
        query = db.query(Job).filter(Job.sent.is_(None)).order_by(Job.date_posted.desc())
        total = query.count()
        items = query.limit(limit).all()
        return {
            "items": [item.to_dict(for_dashboard=True) for item in items],
            "total": total
        }
    
    def get_router(self) -> APIRouter:
        router = APIRouter()
        
        # ============== COMPANIES ==============
        
        @router.get("/companies")
        def get_companies(
            page: int = Query(1, ge=1),
            per_page: int = Query(20, ge=1, le=100),
            location: Optional[str] = None,
            search: Optional[str] = None,
            include_research: bool = False,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            query = db.query(Company).order_by(Company.research_date.desc())
            
            if location:
                query = query.filter(Company.location.ilike(f"%{location}%"))
            if search:
                query = query.filter(Company.title.ilike(f"%{search}%"))
            
            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            
            return {
                "items": [item.to_dict(include_research=include_research) for item in items],
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": (total + per_page - 1) // per_page
            }
        
        @router.get("/companies/{company_id}")
        def get_company(
            company_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Company).filter(Company.id == company_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Company not found")
            return item.to_dict(include_research=True)
        
        @router.post("/companies", status_code=201)
        def create_company(
            data: CompanyCreate,
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            errors = CompanyCreate.validate_required(data.model_dump())
            if errors:
                raise HTTPException(status_code=422, detail={'validation_errors': errors})
            
            item = Company(
                title=data.title,
                location=data.location,
                research_date=parse_date(data.research_date),
                url=data.url,
                research=data.research
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.put("/companies/{company_id}")
        def update_company(
            company_id: int,
            data: CompanyUpdate,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Company).filter(Company.id == company_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Company not found")
            
            if data.title is not None:
                item.title = data.title
            if data.location is not None:
                item.location = data.location
            if data.research_date is not None:
                item.research_date = parse_date(data.research_date)
            if data.url is not None:
                item.url = data.url
            if data.research is not None:
                item.research = data.research
            
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.delete("/companies/{company_id}")
        def delete_company(
            company_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Company).filter(Company.id == company_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Company not found")
            db.delete(item)
            db.commit()
            return {"message": "Company deleted"}
        
        # ============== JOBS ==============
        
        @router.get("/jobs")
        def get_jobs(
            page: int = Query(1, ge=1),
            per_page: int = Query(20, ge=1, le=100),
            company: Optional[str] = None,
            location: Optional[str] = None,
            remote: Optional[str] = None,
            site: Optional[str] = None,
            unsent: Optional[str] = None,
            search: Optional[str] = None,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            query = db.query(Job).order_by(Job.date_posted.desc())
            
            if company:
                query = query.filter(Job.company.ilike(f"%{company}%"))
            if location:
                query = query.filter(Job.location.ilike(f"%{location}%"))
            if remote == "true":
                query = query.filter(Job.is_remote == True)
            if site:
                query = query.filter(Job.site == site)
            if unsent == "true":
                query = query.filter(Job.sent.is_(None))
            if search:
                query = query.filter(or_(
                    Job.title.ilike(f"%{search}%"),
                    Job.company.ilike(f"%{search}%")
                ))
            
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
        
        @router.get("/jobs/{job_id}")
        def get_job(
            job_id: str,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Job).filter(Job.id == job_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Job not found")
            return item.to_dict()
        
        @router.post("/jobs", status_code=201)
        def create_job(
            data: JobCreate,
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            errors = JobCreate.validate_required(data.model_dump())
            if errors:
                raise HTTPException(status_code=422, detail={'validation_errors': errors})
            
            job_id = data.id or str(uuid.uuid4())
            
            item = Job(
                id=job_id,
                title=data.title,
                company=data.company,
                company_id=data.company_id,
                location=data.location,
                salary_min=data.salary_min,
                salary_max=data.salary_max,
                job_url=data.job_url,
                site=data.site,
                date_posted=parse_date(data.date_posted),
                is_remote=data.is_remote,
                description=data.description,
                summary=data.summary,
                sent=parse_date(data.sent)
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.put("/jobs/{job_id}")
        def update_job(
            job_id: str,
            data: JobUpdate,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Job).filter(Job.id == job_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Job not found")
            
            if data.title is not None:
                item.title = data.title
            if data.company is not None:
                item.company = data.company
            if data.company_id is not None:
                item.company_id = data.company_id
            if data.location is not None:
                item.location = data.location
            if data.salary_min is not None:
                item.salary_min = data.salary_min
            if data.salary_max is not None:
                item.salary_max = data.salary_max
            if data.job_url is not None:
                item.job_url = data.job_url
            if data.site is not None:
                item.site = data.site
            if data.date_posted is not None:
                item.date_posted = parse_date(data.date_posted)
            if data.is_remote is not None:
                item.is_remote = data.is_remote
            if data.description is not None:
                item.description = data.description
            if data.summary is not None:
                item.summary = data.summary
            if data.sent is not None:
                item.sent = parse_date(data.sent)
            
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        @router.delete("/jobs/{job_id}")
        def delete_job(
            job_id: str,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)
        ):
            item = db.query(Job).filter(Job.id == job_id).first()
            if not item:
                raise HTTPException(status_code=404, detail="Job not found")
            db.delete(item)
            db.commit()
            return {"message": "Job deleted"}
        
        @router.post("/jobs/pop")
        def pop_job(
            db: Session = Depends(get_db),
            api_key: str = Depends(verify_api_key)
        ):
            """Get one unsent job and mark it as sent."""
            item = db.query(Job).filter(Job.sent.is_(None)).order_by(Job.date_posted.asc()).first()
            if not item:
                raise HTTPException(status_code=204, detail="No unsent jobs available")
            
            item.sent = date.today()
            db.commit()
            db.refresh(item)
            return item.to_dict()
        
        return router
