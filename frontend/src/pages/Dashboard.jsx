import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Music, Calendar, Newspaper, Briefcase, ExternalLink, Eye } from 'lucide-react';
import Modal from '../components/Modal';
import { concertsService, eventsService, newsService, jobsService } from '../services/api';
import { formatDate, formatShortDate } from '../utils/helpers';

function SectionCard({ icon: Icon, title, to, color, children, count }) {
  return (
    <div className="section-card">
      <div className="section-card-header">
        <div className="flex items-center gap-3">
          <div className={`section-icon ${color}`}>
            <Icon className="w-4 h-4 text-white" />
          </div>
          <h2 className="font-semibold text-primary">{title}</h2>
          {count > 0 && (
            <span className="badge badge-gray">{count} unsent</span>
          )}
        </div>
        <Link to={to} className="link text-sm">View all →</Link>
      </div>
      <div className="section-card-body">
        {children}
      </div>
    </div>
  );
}

function ConcertItem({ concert, onView }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        <p className="font-medium text-primary truncate">{concert.artists?.join(', ')}</p>
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{formatShortDate(concert.date)}</span>
          {concert.venue && <span>• {concert.venue}</span>}
        </div>
      </div>
      <div className="flex items-center gap-1">
        <button onClick={() => onView(concert)} className="icon-btn" title="View details">
          <Eye className="w-4 h-4" />
        </button>
        {concert.source_url && (
          <a href={concert.source_url} target="_blank" rel="noopener noreferrer" className="icon-btn" title="Open source">
            <ExternalLink className="w-4 h-4" />
          </a>
        )}
      </div>
    </div>
  );
}

function EventItem({ event, onView }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        <p className="font-medium text-primary truncate">{event.title}</p>
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{formatShortDate(event.date)}</span>
          {event.category && <span className="badge badge-blue">{event.category}</span>}
        </div>
      </div>
      <button onClick={() => onView(event)} className="icon-btn" title="View details">
        <Eye className="w-4 h-4" />
      </button>
    </div>
  );
}

function NewsItem({ item, onView }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        <p className="font-medium text-primary line-clamp-2">{item.title}</p>
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{formatShortDate(item.date)}</span>
          {item.category && <span className="badge badge-green">{item.category}</span>}
        </div>
      </div>
      <button onClick={() => onView(item)} className="icon-btn" title="View details">
        <Eye className="w-4 h-4" />
      </button>
    </div>
  );
}

function JobItem({ job, onView }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        <p className="font-medium text-primary truncate">{job.title}</p>
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{job.company}</span>
          {job.is_remote && <span className="badge badge-green">Remote</span>}
        </div>
      </div>
      <button onClick={() => onView(job)} className="icon-btn" title="View details">
        <Eye className="w-4 h-4" />
      </button>
    </div>
  );
}

function EmptyState({ message }) {
  return <p className="text-muted text-sm py-4 text-center">{message}</p>;
}

export default function Dashboard() {
  const [data, setData] = useState({
    concerts: { items: [], total: 0 },
    events: { items: [], total: 0 },
    news: { items: [], total: 0 },
    jobs: { items: [], total: 0 },
  });
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  const [modalType, setModalType] = useState(null);

  const openModal = (item, type) => {
    setSelectedItem(item);
    setModalType(type);
  };

  const closeModal = () => {
    setSelectedItem(null);
    setModalType(null);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [concerts, events, news, jobs] = await Promise.all([
          concertsService.getAll({ per_page: 3, unsent: 'true' }),
          eventsService.getAll({ per_page: 3, unsent: 'true' }),
          newsService.getAll({ per_page: 3, unsent: 'true' }),
          jobsService.getAll({ per_page: 3, unsent: 'true' }),
        ]);

        setData({
          concerts: { items: concerts.data.items, total: concerts.data.total },
          events: { items: events.data.items, total: events.data.total },
          news: { items: news.data.items, total: news.data.total },
          jobs: { items: jobs.data.items, total: jobs.data.total },
        });
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-secondary">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Welcome back</h1>
        <p className="page-subtitle">Here's what's new from your OpenClaw concierge</p>
      </div>

      <div className="grid-2">
        <SectionCard icon={Music} title="Upcoming Concerts" to="/concerts" color="section-icon-purple" count={data.concerts.total}>
          {data.concerts.items.length > 0 ? (
            data.concerts.items.map((concert) => <ConcertItem key={concert.id} concert={concert} onView={(c) => openModal(c, 'concert')} />)
          ) : (
            <EmptyState message="No new concerts to review" />
          )}
        </SectionCard>

        <SectionCard icon={Calendar} title="Local Events" to="/events" color="section-icon-blue" count={data.events.total}>
          {data.events.items.length > 0 ? (
            data.events.items.map((event) => <EventItem key={event.id} event={event} onView={(e) => openModal(e, 'event')} />)
          ) : (
            <EmptyState message="No new events to review" />
          )}
        </SectionCard>

        <SectionCard icon={Newspaper} title="News Feed" to="/news" color="section-icon-green" count={data.news.total}>
          {data.news.items.length > 0 ? (
            data.news.items.map((item) => <NewsItem key={item.id} item={item} onView={(n) => openModal(n, 'news')} />)
          ) : (
            <EmptyState message="No new articles to review" />
          )}
        </SectionCard>

        <SectionCard icon={Briefcase} title="Job Opportunities" to="/career" color="section-icon-orange" count={data.jobs.total}>
          {data.jobs.items.length > 0 ? (
            data.jobs.items.map((job) => <JobItem key={job.id} job={job} onView={(j) => openModal(j, 'job')} />)
          ) : (
            <EmptyState message="No new jobs to review" />
          )}
        </SectionCard>
      </div>

      <Modal isOpen={!!selectedItem} onClose={closeModal} title={getModalTitle()} size="lg">
        {selectedItem && renderModalContent()}
      </Modal>
    </div>
  );

  function getModalTitle() {
    if (!selectedItem) return '';
    switch (modalType) {
      case 'concert': return 'Concert Details';
      case 'event': return 'Event Details';
      case 'news': return 'Article Details';
      case 'job': return 'Job Details';
      default: return 'Details';
    }
  }

  function renderModalContent() {
    if (!selectedItem) return null;
    
    switch (modalType) {
      case 'concert':
        return (
          <div className="space-y-4">
            <div>
              <label className="form-label">Artists</label>
              <p className="text-primary font-medium">{selectedItem.artists?.join(', ')}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Date</label>
                <p className="text-primary">{formatDate(selectedItem.date)}</p>
              </div>
              <div>
                <label className="form-label">Venue</label>
                <p className="text-primary">{selectedItem.venue || '-'}</p>
              </div>
            </div>
            {selectedItem.city && (
              <div>
                <label className="form-label">City</label>
                <p className="text-primary">{selectedItem.city}</p>
              </div>
            )}
            {selectedItem.source_url && (
              <div>
                <label className="form-label">Source</label>
                <a href={selectedItem.source_url} target="_blank" rel="noopener noreferrer" className="link block truncate">
                  {selectedItem.source_url}
                </a>
              </div>
            )}
          </div>
        );
      
      case 'event':
        return (
          <div className="space-y-4">
            <div>
              <label className="form-label">Title</label>
              <p className="text-primary font-medium">{selectedItem.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Date</label>
                <p className="text-primary">{formatDate(selectedItem.date)}</p>
              </div>
              <div>
                <label className="form-label">Category</label>
                <p className="text-primary capitalize">{selectedItem.category || '-'}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">City</label>
                <p className="text-primary">{selectedItem.city || '-'}</p>
              </div>
              <div>
                <label className="form-label">Venue</label>
                <p className="text-primary">{selectedItem.venue || '-'}</p>
              </div>
            </div>
            {selectedItem.description && (
              <div>
                <label className="form-label">Description</label>
                <p className="text-primary">{selectedItem.description}</p>
              </div>
            )}
            {selectedItem.source_url && (
              <div>
                <label className="form-label">Source</label>
                <a href={selectedItem.source_url} target="_blank" rel="noopener noreferrer" className="link block truncate">
                  {selectedItem.source_url}
                </a>
              </div>
            )}
          </div>
        );
      
      case 'news':
        return (
          <div className="space-y-4">
            <div>
              <label className="form-label">Title</label>
              <p className="text-primary font-medium">{selectedItem.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Date</label>
                <p className="text-primary">{formatDate(selectedItem.date)}</p>
              </div>
              <div>
                <label className="form-label">Category</label>
                <p className="text-primary capitalize">{selectedItem.category || '-'}</p>
              </div>
            </div>
            {selectedItem.summary && (
              <div>
                <label className="form-label">Summary</label>
                <p className="text-primary">{selectedItem.summary}</p>
              </div>
            )}
            {selectedItem.source_url && (
              <div>
                <label className="form-label">Source</label>
                <a href={selectedItem.source_url} target="_blank" rel="noopener noreferrer" className="link block truncate">
                  {selectedItem.source_url}
                </a>
              </div>
            )}
          </div>
        );
      
      case 'job':
        return (
          <div className="space-y-4">
            <div>
              <label className="form-label">Title</label>
              <p className="text-primary font-semibold text-lg">{selectedItem.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Company</label>
                <p className="text-primary">{selectedItem.company}</p>
              </div>
              <div>
                <label className="form-label">Location</label>
                <p className="text-primary">{selectedItem.location || '-'}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Remote</label>
                <p className="text-primary">{selectedItem.is_remote ? 'Yes' : 'No'}</p>
              </div>
              <div>
                <label className="form-label">Posted</label>
                <p className="text-primary">{formatDate(selectedItem.date_posted)}</p>
              </div>
            </div>
            {selectedItem.summary && (
              <div>
                <label className="form-label">Summary</label>
                <p className="text-primary">{selectedItem.summary}</p>
              </div>
            )}
            {selectedItem.job_url && (
              <div>
                <a href={selectedItem.job_url} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
                  <ExternalLink className="w-4 h-4" />
                  View Job Listing
                </a>
              </div>
            )}
          </div>
        );
      
      default:
        return null;
    }
  }
}
