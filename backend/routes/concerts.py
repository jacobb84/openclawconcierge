from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Concert
from routes.auth import api_key_required

concerts_bp = Blueprint('concerts', __name__, url_prefix='/api/concerts')


def parse_date(date_str):
    """Parse date string to date object."""
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


@concerts_bp.route('', methods=['GET'])
@jwt_required()
def get_concerts():
    """Get all concerts with optional filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Concert.query.order_by(Concert.date.desc())
    
    # Optional filters
    if request.args.get('city'):
        query = query.filter(Concert.city.ilike(f"%{request.args.get('city')}%"))
    if request.args.get('venue'):
        query = query.filter(Concert.venue.ilike(f"%{request.args.get('venue')}%"))
    if request.args.get('unsent') == 'true':
        query = query.filter(Concert.sent.is_(None))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [c.to_dict() for c in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@concerts_bp.route('/<int:concert_id>', methods=['GET'])
@jwt_required()
def get_concert(concert_id):
    """Get a single concert by ID."""
    concert = Concert.query.get_or_404(concert_id)
    return jsonify(concert.to_dict()), 200


@concerts_bp.route('', methods=['POST'])
@api_key_required
def create_concert():
    """Create a new concert."""
    data = request.get_json()
    
    if not data or not data.get('artists'):
        return jsonify({'error': 'Artists list required'}), 400
    
    concert = Concert(
        artists=data.get('artists'),
        date=parse_date(data.get('date')),
        venue=data.get('venue'),
        city=data.get('city'),
        source_url=data.get('source_url'),
        sent=parse_date(data.get('sent'))
    )
    
    db.session.add(concert)
    db.session.commit()
    
    return jsonify(concert.to_dict()), 201


@concerts_bp.route('/<int:concert_id>', methods=['PUT'])
@jwt_required()
def update_concert(concert_id):
    """Update an existing concert."""
    concert = Concert.query.get_or_404(concert_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'artists' in data:
        concert.artists = data['artists']
    if 'date' in data:
        concert.date = parse_date(data['date'])
    if 'venue' in data:
        concert.venue = data['venue']
    if 'city' in data:
        concert.city = data['city']
    if 'source_url' in data:
        concert.source_url = data['source_url']
    if 'sent' in data:
        concert.sent = parse_date(data['sent'])
    
    db.session.commit()
    
    return jsonify(concert.to_dict()), 200


@concerts_bp.route('/<int:concert_id>', methods=['DELETE'])
@jwt_required()
def delete_concert(concert_id):
    """Delete a concert."""
    concert = Concert.query.get_or_404(concert_id)
    db.session.delete(concert)
    db.session.commit()
    
    return jsonify({'message': 'Concert deleted'}), 200
