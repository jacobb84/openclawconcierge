import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { jobsService, companiesService } from '../services/api';
import Pagination from '../components/Pagination';
import Modal from '../components/Modal';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  MapPin, Calendar, Trash2, Building2, 
  DollarSign, Briefcase, Globe, FileText
} from 'lucide-react';
import { formatDate, formatSalary } from '../utils/helpers';

function JobsTab({ onViewCompany }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({ total: 0, pages: 1 });

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
              {job.job_url ? (
                <a href={job.job_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-primary mb-1 block link hover:underline">
                  {job.title}
                </a>
              ) : (
                <h3 className="font-semibold text-primary mb-1">{job.title}</h3>
              )}
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
                {job.date_posted && (
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    Posted {formatDate(job.date_posted)}
                  </span>
                )}
              </div>
              {job.summary && (
                <p className="text-secondary text-sm mt-3 line-clamp-2">{job.summary}</p>
              )}
            </div>
            <div className="flex items-center gap-1">
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
      <div className="space-y-4">
        {companies.map((company) => (
          <div key={company.id} className="card p-6">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                {company.url ? (
                  <a href={company.url} target="_blank" rel="noopener noreferrer" className="font-semibold text-primary mb-2 block link hover:underline">
                    {company.title}
                  </a>
                ) : (
                  <h3 className="font-semibold text-primary mb-2">{company.title}</h3>
                )}
                <div className="flex items-center gap-4 text-sm text-muted">
                  {company.location && (
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {company.location}
                    </span>
                  )}
                  {company.research_date && (
                    <span className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      Researched {formatDate(company.research_date)}
                    </span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button onClick={() => handleViewResearch(company)} className="icon-btn" title="View research">
                  <FileText className="w-4 h-4" />
                </button>
                <button onClick={() => handleDelete(company.id)} className="icon-btn icon-btn-danger" title="Delete">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {companies.length === 0 && (
          <div className="card text-center py-12 text-secondary">No companies found</div>
        )}

        <Pagination page={page} pages={pagination.pages} total={pagination.total} onPageChange={fetchCompanies} />
      </div>

      <Modal isOpen={!!selectedCompany || loadingResearch} onClose={() => setSelectedCompany(null)} title={selectedCompany?.title || 'Loading...'} size="xl">
        {loadingResearch ? (
          <div className="flex items-center justify-center h-32">
            <p className="text-secondary">Loading research...</p>
          </div>
        ) : selectedCompany && (
          <div className="space-y-4">
            <div className="flex flex-wrap items-center gap-4 text-sm">
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
              {selectedCompany.research_date && (
                <span className="flex items-center gap-1 text-muted">
                  <Calendar className="w-4 h-4" />
                  Researched {formatDate(selectedCompany.research_date)}
                </span>
              )}
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
            <div className="flex flex-wrap items-center gap-4 text-sm">
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
              {selectedCompany.research_date && (
                <span className="flex items-center gap-1 text-muted">
                  <Calendar className="w-4 h-4" />
                  Researched {formatDate(selectedCompany.research_date)}
                </span>
              )}
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
