import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-neutral-900 border-b border-neutral-800 flex items-center justify-between px-6 z-50">
      <div className="flex items-center gap-6">
        <Link href="/" className="text-xl font-bold tracking-tight text-white hover:opacity-80 transition-opacity">
          Scout
        </Link>
        <div className="hidden md:flex items-center gap-4 text-sm font-medium text-neutral-400">
          <Link href="/dashboard" className="hover:text-white transition-colors">
            Dashboard
          </Link>
          <Link href="/grants" className="hover:text-white transition-colors">
            Grants
          </Link>
          <Link href="/chat" className="hover:text-white transition-colors">
            Agent Chat
          </Link>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="h-8 w-8 rounded-full bg-neutral-800 border border-neutral-700 flex items-center justify-center text-xs font-medium text-white">
          OR
        </div>
      </div>
    </nav>
  );
}
