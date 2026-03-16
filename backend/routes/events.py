from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Event
from routes.auth import api_key_required

events_bp = Blueprint('events', __name__, url_prefix='/api/events')


def parse_date(date_str):
    """Parse date string to date object."""
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


@events_bp.route('', methods=['GET'])
@jwt_required()
def get_events():
    """Get all events with optional filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Event.query.order_by(Event.date.desc())
    
    # Optional filters
    if request.args.get('city'):
        query = query.filter(Event.city.ilike(f"%{request.args.get('city')}%"))
    if request.args.get('category'):
        query = query.filter(Event.category.ilike(f"%{request.args.get('category')}%"))
    if request.args.get('unsent') == 'true':
        query = query.filter(Event.sent.is_(None))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [e.to_dict() for e in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@events_bp.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    """Get a single event by ID."""
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict()), 200


@events_bp.route('', methods=['POST'])
@api_key_required
def create_event():
    """Create a new event."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title required'}), 400
    
    event = Event(
        title=data.get('title'),
        category=data.get('category'),
        summary=data.get('summary'),
        date=parse_date(data.get('date')),
        city=data.get('city'),
        source_url=data.get('source_url'),
        sent=parse_date(data.get('sent'))
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify(event.to_dict()), 201


@events_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    """Update an existing event."""
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        event.title = data['title']
    if 'category' in data:
        event.category = data['category']
    if 'summary' in data:
        event.summary = data['summary']
    if 'date' in data:
        event.date = parse_date(data['date'])
    if 'city' in data:
        event.city = data['city']
    if 'source_url' in data:
        event.source_url = data['source_url']
    if 'sent' in data:
        event.sent = parse_date(data['sent'])
    
    db.session.commit()
    
    return jsonify(event.to_dict()), 200


@events_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    """Delete an event."""
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted'}), 200
