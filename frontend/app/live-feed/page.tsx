'use client';

import { useEffect, useMemo, useState } from 'react';
import { API_BASE } from '../../lib/api';

type FeedItem = { post_id: number; text: string; label: string; confidence: number; created_at: string };

export default function LiveFeedPage() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [labelFilter, setLabelFilter] = useState('All');
  const [threshold, setThreshold] = useState(0);
  const [keyword, setKeyword] = useState('');

  useEffect(() => {
    const ws = new WebSocket(`${API_BASE.replace('http', 'ws')}/ws/live`);
    ws.onmessage = (event) => setItems((prev) => [JSON.parse(event.data), ...prev].slice(0, 100));
    return () => ws.close();
  }, []);

  const filtered = useMemo(
    () =>
      items.filter(
        (item) =>
          (labelFilter === 'All' || item.label === labelFilter) &&
          item.confidence >= threshold &&
          item.text.toLowerCase().includes(keyword.toLowerCase())
      ),
    [items, labelFilter, threshold, keyword]
  );

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">Live Feed</h2>
      <div className="mb-4 grid grid-cols-1 gap-3 md:grid-cols-3">
        <select className="rounded bg-slate-800 p-2" value={labelFilter} onChange={(e) => setLabelFilter(e.target.value)}>
          <option>All</option>
          <option>Likely True</option>
          <option>Likely False</option>
          <option>Uncertain</option>
        </select>
        <input
          type="number"
          className="rounded bg-slate-800 p-2"
          value={threshold}
          onChange={(e) => setThreshold(Number(e.target.value))}
          placeholder="Min confidence"
        />
        <input className="rounded bg-slate-800 p-2" value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="Search keyword" />
      </div>
      <ul className="space-y-3">
        {filtered.map((item) => (
          <li key={item.post_id} className="rounded bg-slate-900 p-3">
            <p>{item.text}</p>
            <span className="mr-3 mt-2 inline-block rounded bg-slate-700 px-2 py-1 text-xs">{item.label}</span>
            <span className="text-xs text-slate-300">{item.confidence}%</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
