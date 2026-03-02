const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function postAnalyzeText(text: string, saveHistory: boolean) {
  const res = await fetch(`${API_BASE}/api/analyze/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, save_history: saveHistory })
  });
  if (!res.ok) throw new Error('Failed to analyze text');
  return res.json();
}

export async function postAnalyzeUrl(url: string, saveHistory: boolean) {
  const res = await fetch(`${API_BASE}/api/analyze/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, save_history: saveHistory })
  });
  if (!res.ok) throw new Error('Failed to analyze URL');
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/api/history`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load history');
  return res.json();
}

export { API_BASE };
