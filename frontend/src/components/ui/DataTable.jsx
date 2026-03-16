/**
 * Reusable Data Table component
 */

export default function DataTable({ columns, data, renderRow, emptyMessage = 'No data found' }) {
  return (
    <div className="card overflow-hidden">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col, i) => (
              <th key={i} className={col.align === 'right' ? 'text-right' : ''}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, i) => renderRow(item, i))}
        </tbody>
      </table>
      
      {data.length === 0 && (
        <div className="text-center py-12 text-secondary">
          {emptyMessage}
        </div>
      )}
    </div>
  );
}
