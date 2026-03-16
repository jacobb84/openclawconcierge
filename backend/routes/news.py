from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, News
from routes.auth import api_key_required

news_bp = Blueprint('news', __name__, url_prefix='/api/news')


def parse_date(date_str):
    """Parse date string to date object."""
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


@news_bp.route('', methods=['GET'])
@jwt_required()
def get_news():
    """Get all news with optional filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = News.query.order_by(News.date.desc())
    
    # Optional filters
    if request.args.get('category'):
        query = query.filter(News.category.ilike(f"%{request.args.get('category')}%"))
    if request.args.get('confirmed') == 'true':
        query = query.filter(News.confirmed == True)
    if request.args.get('confirmed') == 'false':
        query = query.filter(News.confirmed == False)
    if request.args.get('unsent') == 'true':
        query = query.filter(News.sent.is_(None))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [n.to_dict() for n in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@news_bp.route('/pop', methods=['POST'])
@api_key_required
def pop_news():
    """
    Drip feed endpoint: Get one unsent news article and mark it as sent.
    Returns the article with sent date updated to current date.
    """
    news_item = News.query.filter(News.sent.is_(None)).order_by(News.date.asc()).first()
    
    if not news_item:
        return jsonify({'message': 'No unsent news available'}), 204
    
    news_item.sent = date.today()
    db.session.commit()
    
    return jsonify(news_item.to_dict()), 200


@news_bp.route('/<int:news_id>', methods=['GET'])
@jwt_required()
def get_news_item(news_id):
    """Get a single news item by ID."""
    news_item = News.query.get_or_404(news_id)
    return jsonify(news_item.to_dict()), 200


@news_bp.route('', methods=['POST'])
@api_key_required
def create_news():
    """Create a new news item."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title required'}), 400
    
    news_item = News(
        title=data.get('title'),
        category=data.get('category'),
        date=parse_date(data.get('date')),
        sent=parse_date(data.get('sent')),
        summary=data.get('summary'),
        source_url=data.get('source_url'),
        confirmed=data.get('confirmed', False),
        tags=data.get('tags', [])
    )
    
    db.session.add(news_item)
    db.session.commit()
    
    return jsonify(news_item.to_dict()), 201


@news_bp.route('/<int:news_id>', methods=['PUT'])
@jwt_required()
def update_news(news_id):
    """Update an existing news item."""
    news_item = News.query.get_or_404(news_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        news_item.title = data['title']
    if 'category' in data:
        news_item.category = data['category']
    if 'date' in data:
        news_item.date = parse_date(data['date'])
    if 'sent' in data:
        news_item.sent = parse_date(data['sent'])
    if 'summary' in data:
        news_item.summary = data['summary']
    if 'source_url' in data:
        news_item.source_url = data['source_url']
    if 'confirmed' in data:
        news_item.confirmed = data['confirmed']
    if 'tags' in data:
        news_item.tags = data['tags']
    
    db.session.commit()
    
    return jsonify(news_item.to_dict()), 200


@news_bp.route('/<int:news_id>', methods=['DELETE'])
@jwt_required()
def delete_news(news_id):
    """Delete a news item."""
    news_item = News.query.get_or_404(news_id)
    db.session.delete(news_item)
    db.session.commit()
    
    return jsonify({'message': 'News item deleted'}), 200
