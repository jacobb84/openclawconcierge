import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Music, Calendar, Newspaper, Briefcase } from 'lucide-react';
import { pluginsService } from '../services/api';
import { formatShortDate } from '../utils/helpers';

const iconMap = {
  Music,
  Calendar,
  Newspaper,
  Briefcase,
};

function SectionCard({ icon, title, to, color, children }) {
  const Icon = iconMap[icon] || Briefcase;
  return (
    <div className="section-card">
      <div className="section-card-header">
        <div className="flex items-center gap-3">
          <div className={`section-icon section-icon-${color}`}>
            <Icon className="w-4 h-4 text-white" />
          </div>
          <h2 className="font-semibold text-primary">{title}</h2>
        </div>
        <Link to={to} className="link text-sm">View all →</Link>
      </div>
      <div className="section-card-body">
        {children}
      </div>
    </div>
  );
}

function ConcertItem({ concert }) {
  const title = concert.title || concert.artists?.join(', ') || 'Unknown';
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        {concert.source_url ? (
          <a href={concert.source_url} target="_blank" rel="noopener noreferrer" className="font-medium text-primary truncate block link">
            {title}
          </a>
        ) : (
          <p className="font-medium text-primary truncate">{title}</p>
        )}
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{formatShortDate(concert.date)}</span>
          {concert.venue && <span>• {concert.venue}</span>}
        </div>
      </div>
    </div>
  );
}

function EventItem({ event }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        {event.source_url ? (
          <a href={event.source_url} target="_blank" rel="noopener noreferrer" className="font-medium text-primary truncate block link">
            {event.title}
          </a>
        ) : (
          <p className="font-medium text-primary truncate">{event.title}</p>
        )}
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{formatShortDate(event.date)}</span>
          {event.category && <span className="badge badge-blue">{event.category}</span>}
        </div>
      </div>
    </div>
  );
}

function NewsItem({ item }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        {item.source_url ? (
          <a href={item.source_url} target="_blank" rel="noopener noreferrer" className="font-medium text-primary line-clamp-2 link">
            {item.title}
          </a>
        ) : (
          <p className="font-medium text-primary line-clamp-2">{item.title}</p>
        )}
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{formatShortDate(item.date)}</span>
          {item.category && <span className="badge badge-green">{item.category}</span>}
        </div>
      </div>
    </div>
  );
}

function JobItem({ job }) {
  return (
    <div className="dashboard-item">
      <div className="flex-1 min-w-0">
        {job.job_url ? (
          <a href={job.job_url} target="_blank" rel="noopener noreferrer" className="font-medium text-primary truncate block link">
            {job.title}
          </a>
        ) : (
          <p className="font-medium text-primary truncate">{job.title}</p>
        )}
        <div className="flex items-center gap-3 mt-1 text-sm text-secondary">
          <span>{job.company}</span>
          {job.is_remote && <span className="badge badge-green">Remote</span>}
        </div>
      </div>
    </div>
  );
}

function EmptyState({ message }) {
  return <p className="text-muted text-sm py-4 text-center">{message}</p>;
}

export default function Dashboard() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await pluginsService.getDashboard();
        setData(response.data);
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

  const renderItems = (pluginName, items) => {
    switch (pluginName) {
      case 'concerts':
        return items.map((concert) => <ConcertItem key={concert.id} concert={concert} />);
      case 'events':
        return items.map((event) => <EventItem key={event.id} event={event} />);
      case 'news':
        return items.map((item) => <NewsItem key={item.id} item={item} />);
      case 'careers':
        return items.map((job) => <JobItem key={job.id} job={job} />);
      default:
        return items.map((item, idx) => (
          <div key={idx} className="dashboard-item">
            <p className="font-medium text-primary truncate">{item.title || item.name || 'Item'}</p>
          </div>
        ));
    }
  };

  const getEmptyMessage = (pluginName) => {
    switch (pluginName) {
      case 'concerts': return 'No upcoming concerts';
      case 'events': return 'No upcoming events';
      case 'news': return 'No new articles to review';
      case 'careers': return 'No new jobs to review';
      default: return 'No items';
    }
  };

  const sortedPlugins = Object.entries(data).sort((a, b) => {
    const orderMap = { concerts: 1, events: 2, news: 3, careers: 4 };
    return (orderMap[a[0]] || 99) - (orderMap[b[0]] || 99);
  });

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Welcome back</h1>
        <p className="page-subtitle">Here's what's new from your OpenClaw concierge</p>
      </div>

      <div className="grid-2">
        {sortedPlugins.map(([pluginName, pluginData]) => (
          <SectionCard
            key={pluginName}
            icon={pluginData.icon}
            title={pluginData.display_name}
            to={pluginData.route}
            color={pluginData.color}
          >
            {pluginData.items?.length > 0 ? (
              renderItems(pluginName, pluginData.items)
            ) : (
              <EmptyState message={getEmptyMessage(pluginName)} />
            )}
          </SectionCard>
        ))}
      </div>
    </div>
  );
}
