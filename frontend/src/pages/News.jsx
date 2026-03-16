import { useEffect, useState } from 'react';
import { newsService } from '../services/api';
import Pagination from '../components/Pagination';
import Modal from '../components/Modal';
import { ExternalLink, Calendar, Trash2, Eye, Tag, CheckCircle, Clock } from 'lucide-react';

export default function News() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });
  const [selectedNews, setSelectedNews] = useState(null);
  const [filter, setFilter] = useState('all');

  const fetchNews = async (pageNum = 1, filterType = filter) => {
    setLoading(true);
    try {
      const params = { page: pageNum, per_page: 20 };
      if (filterType === 'unsent') params.unsent = 'true';
      if (filterType === 'confirmed') params.confirmed = 'true';
      
      const response = await newsService.getAll(params);
      setNews(response.data.items);
      setPagination({ total: response.data.total, pages: response.data.pages });
      setPage(pageNum);
    } catch (error) {
      console.error('Failed to fetch news:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews(1, filter);
  }, [filter]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this article?')) return;
    try {
      await newsService.delete(id);
      fetchNews(page);
    } catch (error) {
      console.error('Failed to delete news:', error);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Unknown';
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading && news.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Loading news...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">News</h1>
          <p className="text-gray-500 mt-1">News articles and updates</p>
        </div>
        <div className="flex gap-2">
          {['all', 'unsent', 'confirmed'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === f
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {news.map((item) => (
          <div
            key={item.id}
            className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  {item.category && (
                    <span className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-blue-100 text-blue-700 rounded-full">
                      <Tag className="w-3 h-3" />
                      {item.category}
                    </span>
                  )}
                  {item.confirmed ? (
                    <span className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
                      <CheckCircle className="w-3 h-3" />
                      Confirmed
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full">
                      <Clock className="w-3 h-3" />
                      Unconfirmed
                    </span>
                  )}
                  {item.sent && (
                    <span className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">
                      Sent {formatDate(item.sent)}
                    </span>
                  )}
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">{item.title}</h3>
                {item.summary && (
                  <p className="text-gray-600 text-sm mb-3 line-clamp-2">{item.summary}</p>
                )}
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {formatDate(item.date)}
                  </span>
                  {item.tags && item.tags.length > 0 && (
                    <div className="flex gap-1">
                      {item.tags.slice(0, 3).map((tag) => (
                        <span key={tag} className="text-xs bg-gray-100 px-2 py-0.5 rounded">
                          {tag}
                        </span>
                      ))}
                      {item.tags.length > 3 && (
                        <span className="text-xs text-gray-400">+{item.tags.length - 3}</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setSelectedNews(item)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="View details"
                >
                  <Eye className="w-4 h-4 text-gray-500" />
                </button>
                {item.source_url && (
                  <a
                    href={item.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    title="Open source"
                  >
                    <ExternalLink className="w-4 h-4 text-gray-500" />
                  </a>
                )}
                <button
                  onClick={() => handleDelete(item.id)}
                  className="p-2 hover:bg-red-100 rounded-lg transition-colors"
                  title="Delete"
                >
                  <Trash2 className="w-4 h-4 text-red-500" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {news.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-white rounded-xl border border-gray-200">
            No news articles found
          </div>
        )}

        <Pagination
          page={page}
          pages={pagination.pages}
          total={pagination.total}
          onPageChange={(p) => fetchNews(p)}
        />
      </div>

      <Modal
        isOpen={!!selectedNews}
        onClose={() => setSelectedNews(null)}
        title="Article Details"
        size="lg"
      >
        {selectedNews && (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-500">Title</label>
              <p className="text-gray-800 font-medium">{selectedNews.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Category</label>
                <p className="text-gray-800">{selectedNews.category || '-'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Date</label>
                <p className="text-gray-800">{formatDate(selectedNews.date)}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Status</label>
                <p className="text-gray-800">{selectedNews.confirmed ? 'Confirmed' : 'Unconfirmed'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Sent Date</label>
                <p className="text-gray-800">{selectedNews.sent ? formatDate(selectedNews.sent) : 'Not sent'}</p>
              </div>
            </div>
            {selectedNews.summary && (
              <div>
                <label className="text-sm font-medium text-gray-500">Summary</label>
                <p className="text-gray-800">{selectedNews.summary}</p>
              </div>
            )}
            {selectedNews.tags && selectedNews.tags.length > 0 && (
              <div>
                <label className="text-sm font-medium text-gray-500">Tags</label>
                <div className="flex flex-wrap gap-2 mt-1">
                  {selectedNews.tags.map((tag) => (
                    <span key={tag} className="px-2 py-1 bg-gray-100 rounded text-sm">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {selectedNews.source_url && (
              <div>
                <label className="text-sm font-medium text-gray-500">Source</label>
                <a
                  href={selectedNews.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline block truncate"
                >
                  {selectedNews.source_url}
                </a>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}
