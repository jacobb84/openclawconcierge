import { useEffect, useState } from 'react';
import { newsService } from '../services/api';
import Pagination from '../components/Pagination';
import { Calendar, Trash2, Tag, Check, HelpCircle } from 'lucide-react';
import { formatDate } from '../utils/helpers';

export default function News() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });
  const [filter, setFilter] = useState('all');

  const fetchNews = async (pageNum = 1, filterType = filter) => {
    setLoading(true);
    try {
      const params = { page: pageNum, per_page: 20 };
      if (filterType === 'confirmed') params.confirmed = 'true';
      if (filterType === 'unconfirmed') params.confirmed = 'false';
      
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

  if (loading && news.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-secondary">Loading news...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header flex items-center justify-between">
        <div>
          <h1 className="page-title">News</h1>
          <p className="page-subtitle">News articles and updates</p>
        </div>
        <div className="flex gap-2">
          {['all', 'verified', 'unverified'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f === 'verified' ? 'confirmed' : f === 'unverified' ? 'unconfirmed' : f)}
              className={`filter-btn ${filter === (f === 'verified' ? 'confirmed' : f === 'unverified' ? 'unconfirmed' : f) ? 'active' : ''}`}
            >
              <span className="capitalize">{f}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {news.map((item) => (
          <div key={item.id} className="card p-6">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  {item.category && (
                    <span className="badge badge-blue">
                      <Tag className="w-3 h-3" />
                      {item.category}
                    </span>
                  )}
                  {item.confirmed ? (
                    <span className="badge badge-green" title="Fact-checked">
                      <Check className="w-3 h-3" />
                      Verified
                    </span>
                  ) : (
                    <span className="badge badge-yellow" title="Not yet fact-checked">
                      <HelpCircle className="w-3 h-3" />
                      Unverified
                    </span>
                  )}
                </div>
                {item.source_url ? (
                  <a href={item.source_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-primary mb-2 block link hover:underline">
                    {item.title}
                  </a>
                ) : (
                  <h3 className="font-semibold text-primary mb-2">{item.title}</h3>
                )}
                {item.summary && (
                  <p className="text-secondary text-sm mb-3 line-clamp-2">{item.summary}</p>
                )}
                <div className="flex items-center gap-4 text-sm text-muted">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {formatDate(item.date)}
                  </span>
                  {item.tags && item.tags.length > 0 && (
                    <div className="flex gap-1">
                      {item.tags.slice(0, 3).map((tag) => (
                        <span key={tag} className="badge badge-gray">{tag}</span>
                      ))}
                      {item.tags.length > 3 && (
                        <span className="text-xs text-muted">+{item.tags.length - 3}</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button onClick={() => handleDelete(item.id)} className="icon-btn icon-btn-danger" title="Delete">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {news.length === 0 && (
          <div className="card text-center py-12 text-secondary">No news articles found</div>
        )}

        <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={(p) => fetchNews(p)} />
      </div>
    </div>
  );
}
