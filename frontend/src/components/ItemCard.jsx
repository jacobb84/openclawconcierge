import { Trash2 } from 'lucide-react';

export default function ItemCard({ 
  children, 
  onDelete, 
  actions,
  className = '' 
}) {
  return (
    <div className={`card p-6 ${className}`}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {children}
        </div>
        <div className="flex items-center gap-1">
          {actions}
          {onDelete && (
            <button onClick={onDelete} className="icon-btn icon-btn-danger" title="Delete">
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export function CardTitle({ href, children }) {
  if (href) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className="font-semibold text-primary mb-2 block link hover:underline">
        {children}
      </a>
    );
  }
  return <h3 className="font-semibold text-primary mb-2">{children}</h3>;
}

export function CardBadges({ children }) {
  return <div className="flex items-center gap-2 mb-2">{children}</div>;
}

export function CardMeta({ children }) {
  return <div className="flex flex-wrap items-center gap-4 text-sm text-muted">{children}</div>;
}

export function CardSummary({ children }) {
  if (!children) return null;
  return <p className="text-secondary text-sm mt-3 line-clamp-2">{children}</p>;
}
