import { useEffect, useState } from 'react';
import { concertsService } from '../services/api';
import Pagination from '../components/Pagination';
import Modal from '../components/Modal';
import { ExternalLink, MapPin, Calendar, Trash2, Eye } from 'lucide-react';
import { formatDateWithWeekday } from '../utils/helpers';

export default function Concerts() {
  const [concerts, setConcerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });
  const [selectedConcert, setSelectedConcert] = useState(null);

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

      <div className="card overflow-hidden">
        <table className="data-table">
          <thead>
            <tr>
              <th>Artists</th>
              <th>Date</th>
              <th>Venue</th>
              <th>Location</th>
              <th className="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {concerts.map((concert) => (
              <tr key={concert.id}>
                <td>
                  <span className="font-medium text-primary">
                    {concert.artists?.join(', ') || 'Unknown'}
                  </span>
                </td>
                <td>
                  <span className="flex items-center gap-2 text-secondary whitespace-nowrap">
                    <Calendar className="w-4 h-4 flex-shrink-0" />
                    {formatDateWithWeekday(concert.date)}
                  </span>
                </td>
                <td className="text-secondary">{concert.venue || '-'}</td>
                <td>
                  <span className="flex items-center gap-2 text-secondary">
                    <MapPin className="w-4 h-4 flex-shrink-0" />
                    {concert.city || '-'}
                  </span>
                </td>
                <td>
                  <div className="flex items-center justify-end gap-1">
                    <button
                      onClick={() => setSelectedConcert(concert)}
                      className="icon-btn"
                      title="View details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    {concert.source_url && (
                      <a
                        href={concert.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="icon-btn"
                        title="Open source"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    )}
                    <button
                      onClick={() => handleDelete(concert.id)}
                      className="icon-btn icon-btn-danger"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {concerts.length === 0 && (
          <div className="text-center py-12 text-secondary">
            No concerts found
          </div>
        )}

        <div className="card-body">
          <Pagination
            page={page}
            pages={pagination.pages}
            total={pagination.total}
            onPageChange={fetchConcerts}
          />
        </div>
      </div>

      <Modal
        isOpen={!!selectedConcert}
        onClose={() => setSelectedConcert(null)}
        title="Concert Details"
      >
        {selectedConcert && (
          <div className="space-y-4">
            <div>
              <label className="form-label">Artists</label>
              <p className="text-primary">{selectedConcert.artists?.join(', ')}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Date</label>
                <p className="text-primary">{formatDateWithWeekday(selectedConcert.date)}</p>
              </div>
              <div>
                <label className="form-label">Venue</label>
                <p className="text-primary">{selectedConcert.venue || '-'}</p>
              </div>
            </div>
            <div>
              <label className="form-label">Location</label>
              <p className="text-primary">{selectedConcert.city || '-'}</p>
            </div>
            {selectedConcert.source_url && (
              <div>
                <label className="form-label">Source</label>
                <a
                  href={selectedConcert.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link block truncate"
                >
                  {selectedConcert.source_url}
                </a>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}
