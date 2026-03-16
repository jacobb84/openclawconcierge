from datetime import date
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Company, Job
from routes.auth import api_key_required

career_bp = Blueprint('career', __name__, url_prefix='/api/career')


def parse_date(date_str):
    """Parse date string to date object."""
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


# ============== COMPANIES ==============

@career_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    """Get all companies with optional filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    include_research = request.args.get('include_research', 'false') == 'true'
    
    query = Company.query.order_by(Company.research_date.desc())
    
    # Optional filters
    if request.args.get('location'):
        query = query.filter(Company.location.ilike(f"%{request.args.get('location')}%"))
    if request.args.get('search'):
        query = query.filter(Company.title.ilike(f"%{request.args.get('search')}%"))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [c.to_dict(include_research=include_research) for c in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@career_bp.route('/companies/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company(company_id):
    """Get a single company by ID (includes full research document)."""
    company = Company.query.get_or_404(company_id)
    return jsonify(company.to_dict(include_research=True)), 200


@career_bp.route('/companies', methods=['POST'])
@api_key_required
def create_company():
    """Create a new company."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title required'}), 400
    
    company = Company(
        title=data.get('title'),
        location=data.get('location'),
        research_date=parse_date(data.get('research_date')),
        url=data.get('url'),
        research=data.get('research')
    )
    
    db.session.add(company)
    db.session.commit()
    
    return jsonify(company.to_dict()), 201


@career_bp.route('/companies/<int:company_id>', methods=['PUT'])
@jwt_required()
def update_company(company_id):
    """Update an existing company."""
    company = Company.query.get_or_404(company_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        company.title = data['title']
    if 'location' in data:
        company.location = data['location']
    if 'research_date' in data:
        company.research_date = parse_date(data['research_date'])
    if 'url' in data:
        company.url = data['url']
    if 'research' in data:
        company.research = data['research']
    
    db.session.commit()
    
    return jsonify(company.to_dict()), 200


@career_bp.route('/companies/<int:company_id>', methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
    """Delete a company."""
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    
    return jsonify({'message': 'Company deleted'}), 200


# ============== JOBS ==============

@career_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get all jobs with optional filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Job.query.order_by(Job.date_posted.desc())
    
    # Optional filters
    if request.args.get('company'):
        query = query.filter(Job.company.ilike(f"%{request.args.get('company')}%"))
    if request.args.get('location'):
        query = query.filter(Job.location.ilike(f"%{request.args.get('location')}%"))
    if request.args.get('remote') == 'true':
        query = query.filter(Job.is_remote == True)
    if request.args.get('site'):
        query = query.filter(Job.site == request.args.get('site'))
    if request.args.get('unsent') == 'true':
        query = query.filter(Job.sent.is_(None))
    if request.args.get('search'):
        search = request.args.get('search')
        query = query.filter(
            db.or_(
                Job.title.ilike(f"%{search}%"),
                Job.company.ilike(f"%{search}%")
            )
        )
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [j.to_dict() for j in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@career_bp.route('/jobs/<string:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get a single job by ID."""
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict()), 200


@career_bp.route('/jobs', methods=['POST'])
@api_key_required
def create_job():
    """Create a new job."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title required'}), 400
    
    job_id = data.get('id', str(uuid.uuid4()))
    
    job = Job(
        id=job_id,
        title=data.get('title'),
        company=data.get('company'),
        company_id=data.get('company_id'),
        location=data.get('location'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        job_url=data.get('job_url'),
        site=data.get('site'),
        date_posted=parse_date(data.get('date_posted')),
        is_remote=data.get('is_remote', False),
        description=data.get('description'),
        summary=data.get('summary'),
        sent=parse_date(data.get('sent'))
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify(job.to_dict()), 201


@career_bp.route('/jobs/<string:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update an existing job."""
    job = Job.query.get_or_404(job_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        job.title = data['title']
    if 'company' in data:
        job.company = data['company']
    if 'company_id' in data:
        job.company_id = data['company_id']
    if 'location' in data:
        job.location = data['location']
    if 'salary_min' in data:
        job.salary_min = data['salary_min']
    if 'salary_max' in data:
        job.salary_max = data['salary_max']
    if 'job_url' in data:
        job.job_url = data['job_url']
    if 'site' in data:
        job.site = data['site']
    if 'date_posted' in data:
        job.date_posted = parse_date(data['date_posted'])
    if 'is_remote' in data:
        job.is_remote = data['is_remote']
    if 'description' in data:
        job.description = data['description']
    if 'summary' in data:
        job.summary = data['summary']
    if 'sent' in data:
        job.sent = parse_date(data['sent'])
    
    db.session.commit()
    
    return jsonify(job.to_dict()), 200


@career_bp.route('/jobs/<string:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete a job."""
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message': 'Job deleted'}), 200
