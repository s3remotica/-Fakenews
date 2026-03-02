'use client';

import { useState } from 'react';
import { postAnalyzeText, postAnalyzeUrl } from '../../lib/api';

export default function AnalyzePage() {
  const [text, setText] = useState('');
  const [url, setUrl] = useState('');
  const [saveHistory, setSaveHistory] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const runTextAnalysis = async () => {
    try {
      setError('');
      setResult(await postAnalyzeText(text, saveHistory));
    } catch {
      setError('Unable to analyze text right now.');
    }
  };

  const runUrlAnalysis = async () => {
    try {
      setError('');
      setResult(await postAnalyzeUrl(url, saveHistory));
    } catch {
      setError('Unable to analyze URL right now.');
    }
  };

  return (
    <div className="space-y-6">
      <section className="rounded-lg bg-slate-900 p-4">
        <h2 className="mb-2 text-xl font-semibold">Analyze Text</h2>
        <textarea
          maxLength={5000}
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="h-36 w-full rounded bg-slate-800 p-3"
          placeholder="Paste article text..."
        />
        <button onClick={runTextAnalysis} className="mt-3 rounded bg-blue-600 px-4 py-2">
          Analyze Text
        </button>
      </section>

      <section className="rounded-lg bg-slate-900 p-4">
        <h2 className="mb-2 text-xl font-semibold">Analyze URL</h2>
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full rounded bg-slate-800 p-3"
          placeholder="https://example.com/news"
        />
        <button onClick={runUrlAnalysis} className="mt-3 rounded bg-indigo-600 px-4 py-2">
          Analyze URL
        </button>
      </section>

      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" checked={saveHistory} onChange={(e) => setSaveHistory(e.target.checked)} />
        Save this analysis to local history
      </label>

      {error && <p className="text-red-400">{error}</p>}

      {result && (
        <section className="rounded-lg border border-slate-700 bg-slate-900 p-5">
          <h3 className="text-2xl font-bold">{result.label}</h3>
          <p className="text-lg">Confidence: {result.confidence}%</p>
          <p className="mt-2 text-sm text-slate-300">{result.model_notice}</p>
          <div className="mt-4">
            <h4 className="font-semibold">Why this result?</h4>
            <p className="text-sm text-slate-300">{result.explanation}</p>
            <ul className="mt-2 list-disc pl-6 text-sm">
              {result.highlights.map((line: string, i: number) => (
                <li key={i} className="rounded bg-yellow-300/20 p-1 text-yellow-100">
                  {line}
                </li>
              ))}
            </ul>
          </div>
          <div className="mt-4 rounded bg-slate-800 p-3 text-sm">
            <h5 className="font-semibold">Next steps to verify</h5>
            <ul className="list-disc pl-6">
              <li>Check multiple reputable sources.</li>
              <li>Look for official statements or datasets.</li>
              <li>Verify publication date and context.</li>
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}
