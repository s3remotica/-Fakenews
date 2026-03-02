import Link from 'next/link';

const links = [
  { href: '/analyze', label: 'Analyze' },
  { href: '/live-feed', label: 'Live Feed' },
  { href: '/history', label: 'History' }
];

export function NavBar() {
  return (
    <nav className="mb-6 flex gap-4 text-sm">
      {links.map((link) => (
        <Link key={link.href} href={link.href} className="rounded bg-slate-800 px-3 py-2 hover:bg-slate-700">
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
