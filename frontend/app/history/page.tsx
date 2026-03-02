'use client';

import { useEffect, useState } from 'react';
import { fetchHistory } from '../../lib/api';

export default function HistoryPage() {
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    fetchHistory().then(setRows).catch(() => setRows([]));
  }, []);

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">History</h2>
      <ul className="space-y-3">
        {rows.map((row) => (
          <li key={row.id} className="rounded bg-slate-900 p-3">
            <p className="font-semibold">{row.label}</p>
            <p className="text-sm">Confidence: {row.confidence}%</p>
            <p className="text-xs text-slate-300">{new Date(row.created_at).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
