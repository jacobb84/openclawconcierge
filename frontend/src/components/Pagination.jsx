import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function Pagination({ page, pages, total, onPageChange }) {
  if (pages <= 1) return null;

  return (
    <div className="pagination">
      <p className="pagination-info">
        Showing page {page} of {pages} ({total} items)
      </p>
      <div className="pagination-buttons">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page <= 1}
          className="pagination-btn"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </button>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page >= pages}
          className="pagination-btn"
        >
          Next
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
