/**
 * Reusable Icon Button component
 */

export default function IconButton({ 
  icon: Icon, 
  onClick, 
  href, 
  title, 
  variant = 'default',
  className = '' 
}) {
  const classes = `icon-btn ${variant === 'danger' ? 'icon-btn-danger' : ''} ${className}`;
  
  if (href) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className={classes}
        title={title}
      >
        <Icon className="w-4 h-4" />
      </a>
    );
  }
  
  return (
    <button onClick={onClick} className={classes} title={title}>
      <Icon className="w-4 h-4" />
    </button>
  );
}
