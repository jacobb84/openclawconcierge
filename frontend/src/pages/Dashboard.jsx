import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Music, Calendar, Newspaper, Briefcase, Building2 } from 'lucide-react';
import { concertsService, eventsService, newsService, jobsService, companiesService } from '../services/api';

function StatCard({ icon: Icon, label, count, to, color }) {
  return (
    <Link
      to={to}
      className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex items-center gap-4">
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div>
          <p className="text-2xl font-bold text-gray-800">{count}</p>
          <p className="text-gray-500">{label}</p>
        </div>
      </div>
    </Link>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState({
    concerts: 0,
    events: 0,
    news: 0,
    jobs: 0,
    companies: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [concerts, events, news, jobs, companies] = await Promise.all([
          concertsService.getAll({ per_page: 1 }),
          eventsService.getAll({ per_page: 1 }),
          newsService.getAll({ per_page: 1 }),
          jobsService.getAll({ per_page: 1 }),
          companiesService.getAll({ per_page: 1 }),
        ]);

        setStats({
          concerts: concerts.data.total,
          events: events.data.total,
          news: news.data.total,
          jobs: jobs.data.total,
          companies: companies.data.total,
        });
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-500 mt-1">Overview of your OpenClaw data</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          icon={Music}
          label="Concerts"
          count={stats.concerts}
          to="/concerts"
          color="bg-purple-500"
        />
        <StatCard
          icon={Calendar}
          label="Events"
          count={stats.events}
          to="/events"
          color="bg-blue-500"
        />
        <StatCard
          icon={Newspaper}
          label="News Articles"
          count={stats.news}
          to="/news"
          color="bg-green-500"
        />
        <StatCard
          icon={Briefcase}
          label="Job Listings"
          count={stats.jobs}
          to="/career"
          color="bg-orange-500"
        />
        <StatCard
          icon={Building2}
          label="Companies"
          count={stats.companies}
          to="/career?tab=companies"
          color="bg-indigo-500"
        />
      </div>
    </div>
  );
}
