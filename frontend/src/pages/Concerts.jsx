import { useEffect, useState } from 'react';
import { concertsService } from '../services/api';
import Pagination from '../components/Pagination';
import Modal from '../components/Modal';
import { ExternalLink, MapPin, Calendar, Trash2, Eye } from 'lucide-react';

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

  const formatDate = (dateStr) => {
    if (!dateStr) return 'TBD';
    return new Date(dateStr).toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading && concerts.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Loading concerts...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Concerts</h1>
        <p className="text-gray-500 mt-1">Upcoming concerts and shows</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Artists</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Date</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Venue</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Location</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Status</th>
              <th className="text-right px-6 py-3 text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {concerts.map((concert) => (
              <tr key={concert.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="font-medium text-gray-800">
                    {concert.artists?.join(', ') || 'Unknown'}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Calendar className="w-4 h-4" />
                    {formatDate(concert.date)}
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-600">{concert.venue || '-'}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <MapPin className="w-4 h-4" />
                    {concert.city || '-'}
                  </div>
                </td>
                <td className="px-6 py-4">
                  {concert.sent ? (
                    <span className="inline-flex px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
                      Sent
                    </span>
                  ) : (
                    <span className="inline-flex px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full">
                      Pending
                    </span>
                  )}
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => setSelectedConcert(concert)}
                      className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                      title="View details"
                    >
                      <Eye className="w-4 h-4 text-gray-500" />
                    </button>
                    {concert.source_url && (
                      <a
                        href={concert.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                        title="Open source"
                      >
                        <ExternalLink className="w-4 h-4 text-gray-500" />
                      </a>
                    )}
                    <button
                      onClick={() => handleDelete(concert.id)}
                      className="p-2 hover:bg-red-100 rounded-lg transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {concerts.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No concerts found
          </div>
        )}

        <div className="px-6 pb-4">
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
              <label className="text-sm font-medium text-gray-500">Artists</label>
              <p className="text-gray-800">{selectedConcert.artists?.join(', ')}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Date</label>
                <p className="text-gray-800">{formatDate(selectedConcert.date)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Venue</label>
                <p className="text-gray-800">{selectedConcert.venue || '-'}</p>
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500">Location</label>
              <p className="text-gray-800">{selectedConcert.city || '-'}</p>
            </div>
            {selectedConcert.source_url && (
              <div>
                <label className="text-sm font-medium text-gray-500">Source</label>
                <a
                  href={selectedConcert.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline block truncate"
                >
                  {selectedConcert.source_url}
                </a>
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-gray-500">Sent Date</label>
              <p className="text-gray-800">{selectedConcert.sent ? formatDate(selectedConcert.sent) : 'Not sent'}</p>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
