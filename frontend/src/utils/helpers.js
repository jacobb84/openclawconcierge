/**
 * Shared utility functions for the OpenClaw Concierge frontend
 */

/**
 * Format a date string for display
 * @param {string} dateStr - ISO date string
 * @param {object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date
 */
export function formatDate(dateStr, options = {}) {
  if (!dateStr) return 'TBD';
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    ...options
  };
  
  return new Date(dateStr).toLocaleDateString('en-US', defaultOptions);
}

/**
 * Format a date with weekday
 * @param {string} dateStr - ISO date string
 * @returns {string} Formatted date with weekday
 */
export function formatDateWithWeekday(dateStr) {
  return formatDate(dateStr, { weekday: 'short' });
}

/**
 * Format a date showing only month and day
 * @param {string} dateStr - ISO date string
 * @returns {string} Formatted short date
 */
export function formatShortDate(dateStr) {
  return formatDate(dateStr, { year: undefined });
}

/**
 * Format salary range for display
 * @param {number} min - Minimum salary
 * @param {number} max - Maximum salary
 * @returns {string|null} Formatted salary range or null
 */
export function formatSalary(min, max) {
  if (!min && !max) return null;
  
  const fmt = (n) => n ? `$${(n / 1000).toFixed(0)}k` : '';
  
  if (min && max) return `${fmt(min)} - ${fmt(max)}`;
  return min ? `From ${fmt(min)}` : `Up to ${fmt(max)}`;
}

/**
 * Truncate text to a maximum length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export function truncate(text, maxLength = 100) {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

/**
 * Join array items with commas, with "and" before the last item
 * @param {string[]} items - Array of strings
 * @returns {string} Joined string
 */
export function joinWithAnd(items) {
  if (!items || items.length === 0) return '';
  if (items.length === 1) return items[0];
  if (items.length === 2) return items.join(' and ');
  return items.slice(0, -1).join(', ') + ', and ' + items[items.length - 1];
}
