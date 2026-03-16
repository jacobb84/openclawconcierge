import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { jobsService, companiesService } from '../services/api';
import Pagination from '../components/Pagination';
import Modal from '../components/Modal';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  ExternalLink, MapPin, Calendar, Trash2, Eye, Building2, 
  DollarSign, Briefcase, Globe, FileText
} from 'lucide-react';

function JobsTab() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });
  const [selectedJob, setSelectedJob] = useState(null);

  const fetchJobs = async (pageNum = 1) => {
    setLoading(true);
    try {
      const response = await jobsService.getAll({ page: pageNum, per_page: 20 });
      setJobs(response.data.items);
      setPagination({ total: response.data.total, pages: response.data.pages });
      setPage(pageNum);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this job?')) return;
    try {
      await jobsService.delete(id);
      fetchJobs(page);
    } catch (error) {
      console.error('Failed to delete job:', error);
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

  const formatSalary = (min, max) => {
    if (!min && !max) return null;
    const fmt = (n) => n ? `$${(n / 1000).toFixed(0)}k` : '';
    if (min && max) return `${fmt(min)} - ${fmt(max)}`;
    return min ? `From ${fmt(min)}` : `Up to ${fmt(max)}`;
  };

  if (loading && jobs.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Loading jobs...</p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  {job.is_remote && (
                    <span className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
                      <Globe className="w-3 h-3" />
                      Remote
                    </span>
                  )}
                  {job.site && (
                    <span className="inline-flex px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">
                      {job.site}
                    </span>
                  )}
                  {job.sent && (
                    <span className="inline-flex px-2 py-1 text-xs font-medium bg-blue-100 text-blue-600 rounded-full">
                      Sent {formatDate(job.sent)}
                    </span>
                  )}
                </div>
                <h3 className="font-semibold text-gray-800 mb-1">{job.title}</h3>
                <div className="flex items-center gap-2 text-gray-600 mb-2">
                  <Building2 className="w-4 h-4" />
                  {job.company}
                </div>
                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                  {job.location && (
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {job.location}
                    </span>
                  )}
                  {formatSalary(job.salary_min, job.salary_max) && (
                    <span className="flex items-center gap-1">
                      <DollarSign className="w-4 h-4" />
                      {formatSalary(job.salary_min, job.salary_max)}
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    Posted {formatDate(job.date_posted)}
                  </span>
                </div>
                {job.summary && (
                  <p className="text-gray-600 text-sm mt-3 line-clamp-2">{job.summary}</p>
                )}
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setSelectedJob(job)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="View details"
                >
                  <Eye className="w-4 h-4 text-gray-500" />
                </button>
                {job.job_url && (
                  <a
                    href={job.job_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    title="View job listing"
                  >
                    <ExternalLink className="w-4 h-4 text-gray-500" />
                  </a>
                )}
                <button
                  onClick={() => handleDelete(job.id)}
                  className="p-2 hover:bg-red-100 rounded-lg transition-colors"
                  title="Delete"
                >
                  <Trash2 className="w-4 h-4 text-red-500" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {jobs.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-white rounded-xl border border-gray-200">
            No jobs found
          </div>
        )}

        <Pagination
          page={page}
          pages={pagination.pages}
          total={pagination.total}
          onPageChange={fetchJobs}
        />
      </div>

      <Modal
        isOpen={!!selectedJob}
        onClose={() => setSelectedJob(null)}
        title="Job Details"
        size="lg"
      >
        {selectedJob && (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-500">Title</label>
              <p className="text-gray-800 font-semibold text-lg">{selectedJob.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Company</label>
                <p className="text-gray-800">{selectedJob.company}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Location</label>
                <p className="text-gray-800">{selectedJob.location || '-'}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Salary Range</label>
                <p className="text-gray-800">{formatSalary(selectedJob.salary_min, selectedJob.salary_max) || '-'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Remote</label>
                <p className="text-gray-800">{selectedJob.is_remote ? 'Yes' : 'No'}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Posted</label>
                <p className="text-gray-800">{formatDate(selectedJob.date_posted)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Source</label>
                <p className="text-gray-800">{selectedJob.site || '-'}</p>
              </div>
            </div>
            {selectedJob.description && (
              <div>
                <label className="text-sm font-medium text-gray-500">Description</label>
                <div className="mt-2 p-4 bg-gray-50 rounded-lg text-gray-800 text-sm whitespace-pre-wrap max-h-64 overflow-y-auto">
                  {selectedJob.description}
                </div>
              </div>
            )}
            {selectedJob.job_url && (
              <div>
                <a
                  href={selectedJob.job_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  View Job Listing
                </a>
              </div>
            )}
          </div>
        )}
      </Modal>
    </>
  );
}

function CompaniesTab() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [loadingResearch, setLoadingResearch] = useState(false);

  const fetchCompanies = async (pageNum = 1) => {
    setLoading(true);
    try {
      const response = await companiesService.getAll({ page: pageNum, per_page: 20 });
      setCompanies(response.data.items);
      setPagination({ total: response.data.total, pages: response.data.pages });
      setPage(pageNum);
    } catch (error) {
      console.error('Failed to fetch companies:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleViewResearch = async (company) => {
    setLoadingResearch(true);
    try {
      const response = await companiesService.getOne(company.id);
      setSelectedCompany(response.data);
    } catch (error) {
      console.error('Failed to fetch company research:', error);
    } finally {
      setLoadingResearch(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this company?')) return;
    try {
      await companiesService.delete(id);
      fetchCompanies(page);
    } catch (error) {
      console.error('Failed to delete company:', error);
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

  if (loading && companies.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Loading companies...</p>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Company</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Location</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Research Date</th>
              <th className="text-right px-6 py-3 text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {companies.map((company) => (
              <tr key={company.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="font-medium text-gray-800">{company.title}</div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <MapPin className="w-4 h-4" />
                    {company.location || '-'}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Calendar className="w-4 h-4" />
                    {formatDate(company.research_date)}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => handleViewResearch(company)}
                      className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                      title="View research"
                    >
                      <FileText className="w-4 h-4 text-gray-500" />
                    </button>
                    {company.url && (
                      <a
                        href={company.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                        title="Visit website"
                      >
                        <ExternalLink className="w-4 h-4 text-gray-500" />
                      </a>
                    )}
                    <button
                      onClick={() => handleDelete(company.id)}
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

        {companies.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No companies found
          </div>
        )}

        <div className="px-6 pb-4">
          <Pagination
            page={page}
            pages={pagination.pages}
            total={pagination.total}
            onPageChange={fetchCompanies}
          />
        </div>
      </div>

      <Modal
        isOpen={!!selectedCompany || loadingResearch}
        onClose={() => setSelectedCompany(null)}
        title={selectedCompany?.title || 'Loading...'}
        size="xl"
      >
        {loadingResearch ? (
          <div className="flex items-center justify-center h-32">
            <p className="text-gray-500">Loading research...</p>
          </div>
        ) : selectedCompany && (
          <div className="space-y-4">
            <div className="flex items-center gap-4 pb-4 border-b border-gray-200">
              {selectedCompany.location && (
                <span className="flex items-center gap-1 text-gray-600">
                  <MapPin className="w-4 h-4" />
                  {selectedCompany.location}
                </span>
              )}
              {selectedCompany.url && (
                <a
                  href={selectedCompany.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-blue-600 hover:underline"
                >
                  <Globe className="w-4 h-4" />
                  Website
                </a>
              )}
              <span className="flex items-center gap-1 text-gray-500">
                <Calendar className="w-4 h-4" />
                Researched {formatDate(selectedCompany.research_date)}
              </span>
            </div>
            {selectedCompany.research ? (
              <div className="markdown-body">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {selectedCompany.research}
                </ReactMarkdown>
              </div>
            ) : (
              <p className="text-gray-500 italic">No research document available.</p>
            )}
          </div>
        )}
      </Modal>
    </>
  );
}

export default function Career() {
  const [searchParams, setSearchParams] = useSearchParams();
  const tab = searchParams.get('tab') || 'jobs';

  const setTab = (newTab) => {
    setSearchParams({ tab: newTab });
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Career</h1>
        <p className="text-gray-500 mt-1">Job listings and company research</p>
      </div>

      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setTab('jobs')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            tab === 'jobs'
              ? 'bg-blue-100 text-blue-700'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <Briefcase className="w-4 h-4" />
          Jobs
        </button>
        <button
          onClick={() => setTab('companies')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            tab === 'companies'
              ? 'bg-blue-100 text-blue-700'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <Building2 className="w-4 h-4" />
          Companies
        </button>
      </div>

      {tab === 'jobs' ? <JobsTab /> : <CompaniesTab />}
    </div>
  );
}
