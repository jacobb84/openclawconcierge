import { useEffect, useState } from 'react';
import { eventsService } from '../services/api';
import Pagination from '../components/Pagination';
import Modal from '../components/Modal';
import { ExternalLink, MapPin, Calendar, Trash2, Eye, Tag } from 'lucide-react';
import { formatDateWithWeekday } from '../utils/helpers';

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });
  const [selectedEvent, setSelectedEvent] = useState(null);

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

      <div className="card overflow-hidden">
        <table className="data-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Date</th>
              <th>Location</th>
              <th className="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td>
                  <span className="font-medium text-primary truncate block max-w-xs">
                    {event.title}
                  </span>
                </td>
                <td>
                  {event.category && (
                    <span className="badge badge-blue">
                      <Tag className="w-3 h-3" />
                      {event.category}
                    </span>
                  )}
                </td>
                <td>
                  <span className="flex items-center gap-2 text-secondary whitespace-nowrap">
                    <Calendar className="w-4 h-4 flex-shrink-0" />
                    {formatDateWithWeekday(event.date)}
                  </span>
                </td>
                <td>
                  <span className="flex items-center gap-2 text-secondary">
                    <MapPin className="w-4 h-4 flex-shrink-0" />
                    {event.city || '-'}
                  </span>
                </td>
                <td>
                  <div className="flex items-center justify-end gap-1">
                    <button onClick={() => setSelectedEvent(event)} className="icon-btn" title="View details">
                      <Eye className="w-4 h-4" />
                    </button>
                    {event.source_url && (
                      <a href={event.source_url} target="_blank" rel="noopener noreferrer" className="icon-btn" title="Open source">
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    )}
                    <button onClick={() => handleDelete(event.id)} className="icon-btn icon-btn-danger" title="Delete">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {events.length === 0 && (
          <div className="text-center py-12 text-secondary">No events found</div>
        )}

        <div className="card-body">
          <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={fetchEvents} />
        </div>
      </div>

      <Modal isOpen={!!selectedEvent} onClose={() => setSelectedEvent(null)} title="Event Details" size="md">
        {selectedEvent && (
          <div className="space-y-4">
            <div>
              <label className="form-label">Title</label>
              <p className="text-primary">{selectedEvent.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Category</label>
                <p className="text-primary capitalize">{selectedEvent.category || '-'}</p>
              </div>
              <div>
                <label className="form-label">Date</label>
                <p className="text-primary">{formatDateWithWeekday(selectedEvent.date)}</p>
              </div>
            </div>
            <div>
              <label className="form-label">Location</label>
              <p className="text-primary">{selectedEvent.city || '-'}</p>
            </div>
            {selectedEvent.summary && (
              <div>
                <label className="form-label">Summary</label>
                <p className="text-primary">{selectedEvent.summary}</p>
              </div>
            )}
            {selectedEvent.source_url && (
              <div>
                <label className="form-label">Source</label>
                <a href={selectedEvent.source_url} target="_blank" rel="noopener noreferrer" className="link block truncate">
                  {selectedEvent.source_url}
                </a>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}
