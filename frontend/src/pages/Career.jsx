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
import { formatDate, formatSalary } from '../utils/helpers';

function JobsTab({ onViewCompany }) {
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

  if (loading && jobs.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-secondary">Loading jobs...</p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div key={job.id} className="card p-6">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  {job.is_remote && (
                    <span className="badge badge-green">
                      <Globe className="w-3 h-3" />
                      Remote
                    </span>
                  )}
                  {job.site && (
                    <span className="badge badge-gray">{job.site}</span>
                  )}
                </div>
                <h3 className="font-semibold text-primary mb-1">{job.title}</h3>
                <div className="flex items-center gap-2 text-secondary mb-2">
                  <Building2 className="w-4 h-4 flex-shrink-0" />
                  {job.company_id ? (
                    <button onClick={() => onViewCompany(job.company_id)} className="link text-left">
                      {job.company}
                    </button>
                  ) : (
                    <span>{job.company}</span>
                  )}
                </div>
                <div className="flex flex-wrap items-center gap-4 text-sm text-muted">
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
                  <p className="text-secondary text-sm mt-3 line-clamp-2">{job.summary}</p>
                )}
              </div>
              <div className="flex items-center gap-1">
                <button onClick={() => setSelectedJob(job)} className="icon-btn" title="View details">
                  <Eye className="w-4 h-4" />
                </button>
                {job.job_url && (
                  <a href={job.job_url} target="_blank" rel="noopener noreferrer" className="icon-btn" title="View job listing">
                    <ExternalLink className="w-4 h-4" />
                  </a>
                )}
                <button onClick={() => handleDelete(job.id)} className="icon-btn icon-btn-danger" title="Delete">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {jobs.length === 0 && (
          <div className="card text-center py-12 text-secondary">No jobs found</div>
        )}

        <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={fetchJobs} />
      </div>

      <Modal isOpen={!!selectedJob} onClose={() => setSelectedJob(null)} title="Job Details" size="lg">
        {selectedJob && (
          <div className="space-y-4">
            <div>
              <label className="form-label">Title</label>
              <p className="text-primary font-semibold text-lg">{selectedJob.title}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Company</label>
                <p className="text-primary">{selectedJob.company}</p>
              </div>
              <div>
                <label className="form-label">Location</label>
                <p className="text-primary">{selectedJob.location || '-'}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Salary Range</label>
                <p className="text-primary">{formatSalary(selectedJob.salary_min, selectedJob.salary_max) || '-'}</p>
              </div>
              <div>
                <label className="form-label">Remote</label>
                <p className="text-primary">{selectedJob.is_remote ? 'Yes' : 'No'}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Posted</label>
                <p className="text-primary">{formatDate(selectedJob.date_posted)}</p>
              </div>
              <div>
                <label className="form-label">Source</label>
                <p className="text-primary capitalize">{selectedJob.site || '-'}</p>
              </div>
            </div>
            {selectedJob.description && (
              <div>
                <label className="form-label">Description</label>
                <div className="job-description">{selectedJob.description}</div>
              </div>
            )}
            {selectedJob.job_url && (
              <div>
                <a href={selectedJob.job_url} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
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

  if (loading && companies.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-secondary">Loading companies...</p>
      </div>
    );
  }

  return (
    <>
      <div className="card overflow-hidden">
        <table className="data-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Location</th>
              <th>Research Date</th>
              <th className="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {companies.map((company) => (
              <tr key={company.id}>
                <td>
                  <span className="font-medium text-primary">{company.title}</span>
                </td>
                <td>
                  <span className="flex items-center gap-2 text-secondary">
                    <MapPin className="w-4 h-4" />
                    {company.location || '-'}
                  </span>
                </td>
                <td>
                  <span className="flex items-center gap-2 text-secondary">
                    <Calendar className="w-4 h-4" />
                    {formatDate(company.research_date)}
                  </span>
                </td>
                <td>
                  <div className="flex items-center justify-end gap-1">
                    <button onClick={() => handleViewResearch(company)} className="icon-btn" title="View research">
                      <FileText className="w-4 h-4" />
                    </button>
                    {company.url && (
                      <a href={company.url} target="_blank" rel="noopener noreferrer" className="icon-btn" title="Visit website">
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    )}
                    <button onClick={() => handleDelete(company.id)} className="icon-btn icon-btn-danger" title="Delete">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {companies.length === 0 && (
          <div className="text-center py-12 text-secondary">No companies found</div>
        )}

        <div className="card-body">
          <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={fetchCompanies} />
        </div>
      </div>

      <Modal isOpen={!!selectedCompany || loadingResearch} onClose={() => setSelectedCompany(null)} title={selectedCompany?.title || 'Loading...'} size="xl">
        {loadingResearch ? (
          <div className="flex items-center justify-center h-32">
            <p className="text-secondary">Loading research...</p>
          </div>
        ) : selectedCompany && (
          <div className="space-y-4">
            <div className="company-meta">
              {selectedCompany.location && (
                <span className="flex items-center gap-1 text-secondary">
                  <MapPin className="w-4 h-4" />
                  {selectedCompany.location}
                </span>
              )}
              {selectedCompany.url && (
                <a href={selectedCompany.url} target="_blank" rel="noopener noreferrer" className="link flex items-center gap-1">
                  <Globe className="w-4 h-4" />
                  Website
                </a>
              )}
              <span className="flex items-center gap-1 text-muted">
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
              <p className="text-muted italic">No research document available.</p>
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
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [loadingResearch, setLoadingResearch] = useState(false);

  const setTab = (newTab) => {
    setSearchParams({ tab: newTab });
  };

  const handleViewCompany = async (companyId) => {
    setLoadingResearch(true);
    try {
      const response = await companiesService.getOne(companyId);
      setSelectedCompany(response.data);
    } catch (error) {
      console.error('Failed to fetch company research:', error);
    } finally {
      setLoadingResearch(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Career</h1>
        <p className="page-subtitle">Job listings and company research</p>
      </div>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('jobs')} className={`filter-btn flex items-center gap-2 ${tab === 'jobs' ? 'active' : ''}`}>
          <Briefcase className="w-4 h-4" />
          Jobs
        </button>
        <button onClick={() => setTab('companies')} className={`filter-btn flex items-center gap-2 ${tab === 'companies' ? 'active' : ''}`}>
          <Building2 className="w-4 h-4" />
          Companies
        </button>
      </div>

      {tab === 'jobs' ? <JobsTab onViewCompany={handleViewCompany} /> : <CompaniesTab />}

      <Modal isOpen={!!selectedCompany || loadingResearch} onClose={() => setSelectedCompany(null)} title={selectedCompany?.title || 'Loading...'} size="xl">
        {loadingResearch ? (
          <div className="flex items-center justify-center h-32">
            <p className="text-secondary">Loading research...</p>
          </div>
        ) : selectedCompany && (
          <div className="space-y-4">
            <div className="company-meta">
              {selectedCompany.location && (
                <span className="flex items-center gap-1 text-secondary">
                  <MapPin className="w-4 h-4" />
                  {selectedCompany.location}
                </span>
              )}
              {selectedCompany.url && (
                <a href={selectedCompany.url} target="_blank" rel="noopener noreferrer" className="link flex items-center gap-1">
                  <Globe className="w-4 h-4" />
                  Website
                </a>
              )}
              <span className="flex items-center gap-1 text-muted">
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
              <p className="text-muted italic">No research document available.</p>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}
