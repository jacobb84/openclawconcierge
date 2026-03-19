import { useEffect, useState } from 'react';
import { concertsService } from '../services/api';
import Pagination from '../components/Pagination';
import { MapPin, Calendar, Trash2 } from 'lucide-react';
import { formatDateWithWeekday } from '../utils/helpers';

export default function Concerts() {
  const [concerts, setConcerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });

  const fetchConcerts = async (pageNum = 1) => {
    setLoading(true);
    try {
      const response = await concertsService.getAll({ page: pageNum, per_page: 20 });
      setConcerts(response.data.items);
      setPagination({ total: response.data.total, pages: response.data.pages });
      setPage(pageNum);
    } catch (error) {
      console.error('Failed to fetch concerts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConcerts();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this concert?')) return;
    try {
      await concertsService.delete(id);
      fetchConcerts(page);
    } catch (error) {
      console.error('Failed to delete concert:', error);
    }
  };

  if (loading && concerts.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-secondary">Loading concerts...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Concerts</h1>
        <p className="page-subtitle">Upcoming concerts and shows</p>
      </div>

      <div className="space-y-4">
        {concerts.map((concert) => (
          <div key={concert.id} className="card p-6">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                {concert.source_url ? (
                  <a href={concert.source_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-primary mb-2 block link hover:underline">
                    {concert.artists?.join(', ') || 'Unknown'}
                  </a>
                ) : (
                  <h3 className="font-semibold text-primary mb-2">{concert.artists?.join(', ') || 'Unknown'}</h3>
                )}
                <div className="flex items-center gap-4 text-sm text-muted">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {formatDateWithWeekday(concert.date)}
                  </span>
                  {concert.venue && (
                    <span className="text-secondary">{concert.venue}</span>
                  )}
                  {concert.city && (
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {concert.city}
                    </span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button onClick={() => handleDelete(concert.id)} className="icon-btn icon-btn-danger" title="Delete">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {concerts.length === 0 && (
          <div className="card text-center py-12 text-secondary">No concerts found</div>
        )}

        <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={fetchConcerts} />
      </div>
    </div>
  );
}
