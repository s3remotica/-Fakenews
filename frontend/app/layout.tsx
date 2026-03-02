import './globals.css';
import { DisclaimerBanner } from '../components/DisclaimerBanner';
import { NavBar } from '../components/NavBar';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="mx-auto min-h-screen max-w-5xl px-4 py-6">
          <h1 className="mb-2 text-3xl font-bold">Real-Time Fake News & Misinformation Detection</h1>
          <p className="mb-4 text-sm text-slate-300">Neutral AI assistance for news credibility checks.</p>
          <DisclaimerBanner />
          <NavBar />
          {children}
        </main>
      </body>
    </html>
  );
}
