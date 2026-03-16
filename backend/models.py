from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Concert(db.Model):
    __tablename__ = 'concerts'
    
    id = db.Column(db.Integer, primary_key=True)
    artists = db.Column(db.JSON, nullable=False)  # List of artist names
    date = db.Column(db.Date, nullable=True)
    venue = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    sent = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'artists': self.artists,
            'date': self.date.isoformat() if self.date else None,
            'venue': self.venue,
            'city': self.city,
            'source_url': self.source_url,
            'sent': self.sent.isoformat() if self.sent else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    sent = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'summary': self.summary,
            'date': self.date.isoformat() if self.date else None,
            'city': self.city,
            'source_url': self.source_url,
            'sent': self.sent.isoformat() if self.sent else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, nullable=True)
    sent = db.Column(db.Date, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    source_url = db.Column(db.String(1000), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    tags = db.Column(db.JSON, nullable=True)  # List of tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'sent': self.sent.isoformat() if self.sent else None,
            'summary': self.summary,
            'source_url': self.source_url,
            'confirmed': self.confirmed,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    research_date = db.Column(db.Date, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    research = db.Column(db.Text, nullable=True)  # Large markdown document
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    jobs = db.relationship('Job', backref='company_ref', lazy='dynamic')
    
    def to_dict(self, include_research=True):
        result = {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'research_date': self.research_date.isoformat() if self.research_date else None,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_research:
            result['research'] = self.research
        return result


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.String(50), primary_key=True)  # UUID from external source
    title = db.Column(db.String(300), nullable=False)
    company = db.Column(db.String(300), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    salary_min = db.Column(db.Float, nullable=True)
    salary_max = db.Column(db.Float, nullable=True)
    job_url = db.Column(db.String(500), nullable=True)
    site = db.Column(db.String(50), nullable=True)
    date_posted = db.Column(db.Date, nullable=True)
    is_remote = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    sent = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'company_id': self.company_id,
            'location': self.location,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'job_url': self.job_url,
            'site': self.site,
            'date_posted': self.date_posted.isoformat() if self.date_posted else None,
            'is_remote': self.is_remote,
            'description': self.description,
            'summary': self.summary,
            'sent': self.sent.isoformat() if self.sent else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
