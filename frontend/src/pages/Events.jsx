import { useEffect, useState } from 'react';
import { eventsService } from '../services/api';
import Pagination from '../components/Pagination';
import { MapPin, Calendar, Trash2, Tag } from 'lucide-react';
import { formatDateWithWeekday } from '../utils/helpers';

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });

  const fetchEvents = async (pageNum = 1) => {
    setLoading(true);
    try {
      const response = await eventsService.getAll({ page: pageNum, per_page: 20 });
      setEvents(response.data.items);
      setPagination({ total: response.data.total, pages: response.data.pages });
      setPage(pageNum);
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this event?')) return;
    try {
      await eventsService.delete(id);
      fetchEvents(page);
    } catch (error) {
      console.error('Failed to delete event:', error);
    }
  };

  if (loading && events.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-secondary">Loading events...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Events</h1>
        <p className="page-subtitle">Local events and exhibitions</p>
      </div>

      <div className="space-y-4">
        {events.map((event) => (
          <div key={event.id} className="card p-6">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  {event.category && (
                    <span className="badge badge-blue">
                      <Tag className="w-3 h-3" />
                      {event.category}
                    </span>
                  )}
                </div>
                {event.source_url ? (
                  <a href={event.source_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-primary mb-2 block link hover:underline">
                    {event.title}
                  </a>
                ) : (
                  <h3 className="font-semibold text-primary mb-2">{event.title}</h3>
                )}
                {event.summary && (
                  <p className="text-secondary text-sm mb-3 line-clamp-2">{event.summary}</p>
                )}
                <div className="flex items-center gap-4 text-sm text-muted">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {formatDateWithWeekday(event.date)}
                  </span>
                  {event.venue && (
                    <span className="text-secondary">{event.venue}</span>
                  )}
                  {event.city && (
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {event.city}
                    </span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button onClick={() => handleDelete(event.id)} className="icon-btn icon-btn-danger" title="Delete">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {events.length === 0 && (
          <div className="card text-center py-12 text-secondary">No events found</div>
        )}

        <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={fetchEvents} />
      </div>
    </div>
  );
}
