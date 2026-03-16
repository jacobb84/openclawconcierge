/**
 * Reusable Badge component
 * Uses CSS classes from index.css for styling
 */

export default function Badge({ children, variant = 'gray', icon: Icon, className = '' }) {
  return (
    <span className={`badge badge-${variant} ${className}`}>
      {Icon && <Icon className="w-3 h-3 flex-shrink-0" />}
      {children}
    </span>
  );
}
